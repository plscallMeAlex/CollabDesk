from api.models import Task, Guild, User
from api.serializers.task_serializer import TaskSerializer, TaskCreateSerializer
from api.tasksmail import update_scheduled_email, cancel_scheduled_email
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime
import os
import pytz


class TaskViewSet(ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    # create a task
    @action(detail=False, methods=["POST"])
    def create_task(self, request):
        title = request.data.get("title", "").strip()
        guild = request.data.get("guild")
        guild = Guild.objects.filter(id=guild).first()

        # Check if the title already exists
        if Task.objects.filter(title__iexact=title, guild=guild).exists():
            return Response(
                {"error": "Task already exists"}, status=status.HTTP_400_BAD_REQUEST
            )

        # Use TaskCreateSerializer for validation
        serializer = TaskCreateSerializer(data=request.data)
        if serializer.is_valid():
            task = serializer.save()
            return Response(TaskSerializer(task).data, status=status.HTTP_201_CREATED)

        # Return validation errors if serializer is not valid
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # get all tasks in a guild
    @action(detail=False, methods=["GET"])
    def in_guild(self, request):
        guild_id = request.query_params.get("guild_id")
        guild = Guild.objects.filter(id=guild_id).first()
        if guild is None:
            return Response(
                {"error": "Guild not found"}, status=status.HTTP_404_NOT_FOUND
            )
        tasks = Task.objects.filter(guild=guild)
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # get all tasks in a guild assigned by a user
    @action(detail=False, methods=["GET"])
    def in_guild_by_assigner(self, request):
        guild_id = request.query_params.get("guild_id")
        assigner_id = request.query_params.get("assigner_id")
        guild = Guild.objects.filter(id=guild_id).first()
        if guild is None:
            return Response(
                {"error": "Guild not found"}, status=status.HTTP_404_NOT_FOUND
            )
        assigner = User.objects.filter(id=assigner_id).first()
        if assigner is None:
            return Response(
                {"error": "Assigner not found"}, status=status.HTTP_404_NOT_FOUND
            )
        tasks = Task.objects.filter(guild=guild, assigner=assigner)
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # get all tasks in a guild assigned to a user
    @action(detail=False, methods=["GET"])
    def in_guild_by_assignee(self, request):
        guild_id = request.query_params.get("guild_id")
        assignee_id = request.query_params.get("assignee_id")
        guild = Guild.objects.filter(id=guild_id).first()
        if guild is None:
            return Response(
                {"error": "Guild not found"}, status=status.HTTP_404_NOT_FOUND
            )
        assignee = User.objects.filter(id=assignee_id).first()
        if assignee is None:
            return Response(
                {"error": "Assignee not found"}, status=status.HTTP_404_NOT_FOUND
            )
        tasks = Task.objects.filter(guild=guild, assignee=assignee)
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # get all tasks in a guild with a specific state
    @action(detail=False, methods=["GET"])
    def in_guild_by_state(self, request):
        state_id = request.query_params.get("state_id")
        tasks = Task.objects.filter(state=state_id)
        if tasks is None:
            return Response(
                {"error": "Tasks not found"}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["GET"])
    def user_tasks(self, request):
        user_id = request.query_params.get("user_id")
        tasks = Task.objects.filter(assignee=user_id)
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # update a task

    @action(detail=True, methods=["PATCH"])
    def update_task(self, request, pk=None):
        task = Task.objects.filter(id=pk).first()
        if task is None:
            return Response(
                {"error": "Task not found"}, status=status.HTTP_404_NOT_FOUND
            )

        # Store the old announce date before serializing
        old_date = task.announce_date

        serializer = TaskSerializer(task, data=request.data, partial=True)
        if serializer.is_valid():
            # Save the updated task first
            updated_task = serializer.save()

            # Check if announce_date was in the request data and handle email
            if "announce_date" in request.data:
                new_date = (
                    updated_task.announce_date
                )  # Get from model instance, not serializer data
                if old_date != new_date:
                    # Pass the serialized task data
                    self.sending_mail(serializer.data, new_date)

            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=["DELETE"])
    def delete_task(self, request, pk=None):
        task = Task.objects.filter(id=pk).first()

        if not task:
            return Response(
                {"error": "Task not found"}, status=status.HTTP_404_NOT_FOUND
            )

        task.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def sending_mail(self, task_data, new_date):
        task_id = task_data.get("id")

        # Cancel the existing email if date is None
        if new_date is None:
            cancel_scheduled_email(task_id)
            return

        # Get related objects properly
        assignee_id = task_data.get("assignee")
        assigner_id = task_data.get("assigner")
        guild_id = task_data.get("guild")

        # Get actual model objects
        guild = Guild.objects.filter(id=guild_id).first()
        assignee = User.objects.filter(id=assignee_id).first()
        assigner = User.objects.filter(id=assigner_id).first()

        # Validate that we have all needed objects
        if not all([guild, assignee, assigner]):
            print(f"Error: Missing related objects for task {task_id}")
            return

        # Format the due date
        due_date = task_data.get("due_date")
        try:
            if due_date:
                # Parse the date string to datetime object
                if isinstance(due_date, str):
                    utc_time = datetime.fromisoformat(due_date.replace("Z", "+00:00"))
                else:
                    utc_time = due_date

                # Convert to Bangkok time
                bangkok_tz = pytz.timezone("Asia/Bangkok")
                bangkok_time = utc_time.astimezone(bangkok_tz)
                formatted_time = bangkok_time.strftime("%b %d, %Y - %I:%M %p")
            else:
                formatted_time = "No due date"
        except Exception as e:
            print(f"Error formatting timestamp: {e}")
            formatted_time = str(due_date)  # Fallback

        # Create email content
        title = task_data.get("title", "Untitled Task")
        description = task_data.get("description", "No description")

        subject = f"Reminded: {title} Task"
        message = f"""
    Task: {title}
    Description: {description}
    Assigner: {assigner.username}
    Guild: {guild.name}
    Due Date: {formatted_time}
        """

        # Get email settings
        from_email = os.getenv("EMAIL_HOST_USER")
        recipient_list = [assignee.email]

        # Add assigner to recipients if they have an email
        if assigner.email and assigner.email != assignee.email:
            recipient_list.append(assigner.email)

        # Schedule or update the email
        update_scheduled_email(
            task_id, subject, message, from_email, recipient_list, new_date
        )
