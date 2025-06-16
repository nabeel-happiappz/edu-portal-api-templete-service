from rest_framework import serializers
from users.models import GuestProfile
from users.serializers import GuestProfileSerializer
from exams.serializers import QuestionSerializer, AnswerSerializer
from exams.models import Question, Answer
from .models import DemoSession, DemoAnswer
import random


class DemoSessionSerializer(serializers.ModelSerializer):
    guest = GuestProfileSerializer(read_only=True)
    
    class Meta:
        model = DemoSession
        fields = ('id', 'guest', 'start_time', 'end_time', 'is_completed')
        read_only_fields = ('id', 'start_time', 'end_time', 'is_completed')


class DemoAnswerSerializer(serializers.ModelSerializer):
    question_text = serializers.CharField(source='question.content', read_only=True)
    
    class Meta:
        model = DemoAnswer
        fields = ('id', 'question', 'question_text', 'selected_answer', 'is_correct', 'answered_at')
        read_only_fields = ('id', 'is_correct', 'answered_at')


class DemoQuestionListSerializer(serializers.Serializer):
    """
    Serializer for returning a list of demo questions
    """
    questions = QuestionSerializer(many=True, read_only=True)
    
    def to_representation(self, instance):
        """
        Get questions for the demo session
        - 10 questions of each type (1-6), for a total of 60 questions
        """
        data = super().to_representation(instance)
        
        # Get the guest profile
        guest = instance.guest
        
        if guest.demo_used:
            return {"error": "Demo already used", "questions": []}
        
        questions_by_type = {}
        result_questions = []
        
        # Get 10 questions of each type
        for q_type in range(1, 7):
            # Get all questions of this type
            type_questions = list(Question.objects.filter(question_type=q_type))
            
            # Randomly select 10 questions (or all if less than 10)
            if len(type_questions) > 10:
                selected = random.sample(type_questions, 10)
            else:
                selected = type_questions
                
            questions_by_type[q_type] = selected
            result_questions.extend(selected)
        
        # Serialize the questions
        data['questions'] = QuestionSerializer(result_questions, many=True).data
        
        return data


class DemoSubmitSerializer(serializers.Serializer):
    """
    Serializer for submitting demo answers
    """
    answers = serializers.ListField(
        child=serializers.DictField(
            child=serializers.IntegerField(),
            allow_empty=False
        ),
        required=True
    )
    
    def validate_answers(self, value):
        """
        Validate the answers format
        """
        for answer_data in value:
            if 'question_id' not in answer_data or 'answer_id' not in answer_data:
                raise serializers.ValidationError(
                    "Each answer must contain 'question_id' and 'answer_id'"
                )
        return value
    
    def save(self, **kwargs):
        """
        Save the demo answers and mark the demo as used
        """
        session = kwargs.get('session')
        answers_data = self.validated_data.get('answers')
        
        # Process each answer
        for answer_data in answers_data:
            question_id = answer_data.get('question_id')
            answer_id = answer_data.get('answer_id')
            
            try:
                question = Question.objects.get(id=question_id)
                answer = Answer.objects.get(id=answer_id)
                
                # Check if the answer is correct
                is_correct = answer.is_correct
                
                # Save the answer
                DemoAnswer.objects.create(
                    session=session,
                    question=question,
                    selected_answer=answer,
                    is_correct=is_correct
                )
                
            except (Question.DoesNotExist, Answer.DoesNotExist):
                # Skip invalid questions/answers
                continue
        
        # Mark the demo as used and update questions attempted
        guest = session.guest
        guest.demo_used = True
        guest.demo_questions_attempted = DemoAnswer.objects.filter(session=session).count()
        guest.save()
        
        # Mark the session as completed
        session.is_completed = True
        session.save()
        
        return session
