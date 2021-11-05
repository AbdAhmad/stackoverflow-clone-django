from django.shortcuts import redirect, render
from .models import Question, Answer, Profile, Questionvote, Answervote, Tags
from .forms import AnswerForm, ProfileForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages


@login_required
def ask(request):
    if request.method == 'POST':
        user = request.user
        title = request.POST['title']
        body = request.POST['body']
        tags = request.POST['tags']
        question = Question(title=title, body=body, author=user)
        question.save()
        all_tags = tags.split()
        for tag in all_tags:
            try:
                tag = Tags.objects.get(tag_word=tag)
                question.tags.add(tag)
            except Exception:
                question.tags.create(tag_word=tag)
            question.save()
        messages.success(request, 'Question Posted')
        return redirect('question', slug=question.slug)
    else:
        return render(request, 'ask.html')


@login_required
def questions(request):
    if request.method == 'POST':
        searched_ques = request.POST['search']
        questions = Question.objects.filter(title__icontains=searched_ques)
        marked = ''
    else:
        if request.GET and ('q' in request.GET) and request.GET['q'] == 'latest':
            questions = Question.objects.all().order_by('-created_at')
            marked = 'latest'
        else:
            questions = Question.objects.all().order_by('-views')
            marked = 'mostviewed'
    questions_dict = {}
    for question in questions:
        ans_n_votes = []
        ans_count = Answer.objects.filter(question_to_ans=question).count()
        all_votes = Questionvote.objects.filter(question=question)
        upvotes = all_votes.filter(upvote=True).count()
        downvotes = all_votes.filter(downvote=True).count()
        votes_count = upvotes - downvotes
        ans_n_votes.append(ans_count)
        ans_n_votes.append(votes_count)
        questions_dict[question] = ans_n_votes

    context = {
        'questions_dict': questions_dict,
        'marked': marked
    }

    return render(request, 'questions.html', context)


@login_required
def question(request, slug):
    question = Question.objects.get(slug=slug)
    user = request.user
    author = question.author
    authenticated = False
    if str(user) == str(author):
        authenticated = True
    all_ques_votes = Questionvote.objects.filter(question=question)
    upvotes = all_ques_votes.filter(upvote=True).count()
    downvotes = all_ques_votes.filter(downvote=True).count()
    ques_votes = upvotes - downvotes
    question.views = question.views + 1 
    question.save()
    answers = Answer.objects.filter(question_to_ans=question)

    answers_votes = {}
    for answer in answers:
        all_ans_votes = Answervote.objects.filter(answer=answer)
        upvotes = all_ans_votes.filter(upvote=True).count()
        downvotes = all_ans_votes.filter(downvote=True).count()
        ans_votes = upvotes - downvotes
        answers_votes[answer] = ans_votes

    if request.method == 'POST':
        form = AnswerForm(data=request.POST)
        if form.is_valid():
            form = form.save(commit = False)
            form.answered_by = request.user
            form.question_to_ans = question
            form.save()
            messages.success(request, 'Answer submitted')
            return redirect('question', slug=slug)
    else:
        form = AnswerForm()   
    context = {
        'question': question,
        'form': form,
        'answers': answers,
        'ques_votes': ques_votes,
        'answers_votes': answers_votes,
        'authenticated': authenticated 
        }
    return render(request, 'question.html', context)


@login_required
def upvote_ques(request, id):
    question = Question.objects.get(id=id)
    user = request.user
    slug = question.slug
    try:
        ques_vote_by_user = Questionvote.objects.filter(user=user)
        ques_vote = ques_vote_by_user.get(question=question)
    except Questionvote.DoesNotExist:
        ques_vote = None
    if ques_vote is not None:
        if ques_vote.upvote != True:
            ques_vote.upvote = True
            ques_vote.downvote = False
            ques_vote.save()  
            messages.success(request, 'You have upvoted this question')
        else:
            messages.info(request, 'You have already upvoted this question')
        return redirect('question', slug=slug)

    vote = Questionvote.objects.create(user=user, question=question, upvote=True, downvote=False)
    vote.save()
    messages.success(request, 'You have upvoted this question')    
    return redirect('question', slug=slug)


@login_required
def downvote_ques(request, id):
    question = Question.objects.get(id=id)
    user = request.user
    slug = question.slug
    try:
        ques_vote_by_user = Questionvote.objects.filter(user=user)
        ques_vote = ques_vote_by_user.get(question=question)
    except Questionvote.DoesNotExist:
        ques_vote = None  
    if ques_vote is not None: 
        if ques_vote.downvote != True:
            ques_vote.downvote = True
            ques_vote.upvote = False
            ques_vote.save() 
            messages.success(request, 'You have downvoted this question')
        else:
            messages.info(request, 'You have already downvoted this question')
        return redirect('question', slug=slug)

    vote = Questionvote.objects.create(user=user, question=question, upvote=False, downvote=True)
    vote.save()
    messages.success(request, 'You have downvoted this question')    
    return redirect('question', slug=slug)


@login_required
def upvote_ans(request, id):
    answer = Answer.objects.get(id=id)
    question = answer.question_to_ans
    slug = question.slug
    user = request.user
    try:
        ans_vote_by_user = Answervote.objects.filter(user=user)
        ans_vote = ans_vote_by_user.get(answer=answer)
    except Answervote.DoesNotExist:
        ans_vote = None

    if ans_vote is not None:
        if ans_vote.user == user:
            if ans_vote.upvote != True: 
                ans_vote.upvote = True
                ans_vote.downvote = False
                ans_vote.save()
                messages.success(request, 'You have upvoted this answer')
            else:
                messages.info(request, 'You have already upvoted this answer')
            return redirect('question', slug=slug)

    vote = Answervote.objects.create(user=user,answer=answer,upvote=True,downvote=False)
    vote.save()
    messages.success(request, 'You have upvoted this answer')    
    return redirect('question', slug=slug)


@login_required
def downvote_ans(request, id):
    answer = Answer.objects.get(id=id)
    question = answer.question_to_ans
    slug = question.slug
    user = request.user
    try:
        ans_vote_by_user = Answervote.objects.filter(user=user)
        ans_vote = ans_vote_by_user.get(answer=answer)
    except Answervote.DoesNotExist:
        ans_vote = None

    if ans_vote is not None: 
        if ans_vote.downvote != True:
            ans_vote.downvote = True
            ans_vote.upvote = False
            ans_vote.save()
            messages.success(request, 'You have downvoted this answer')
        else:
            messages.info(request, 'You have already downvoted this answer')
        return redirect('question', slug=slug)

    vote = Answervote.objects.create(user=user, answer=answer, upvote=False, downvote=True)
    vote.save()
    messages.success(request, 'You have downvoted this question')    
    return redirect('question', slug=slug)


@login_required
def profile(request, author):
    user = request.user
    authenticated = False
    if str(user) == author:
        authenticated = True
    profile = Profile.objects.get(user__username=author)
    questions = Question.objects.filter(author__username=author)
    answers = Answer.objects.filter(answered_by__username=author)
        
    context = {
        'profile': profile,
        'questions': questions,
        'answers': answers,
        'authenticated': authenticated
        }

    return render(request, 'profile.html', context)


@login_required
def edit_profile(request, id):
    profile = Profile.objects.get(id=id)
    author = profile.user.username
    if request.method == 'GET':
        form = ProfileForm(instance=profile)
    else:
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
        messages.success(request, 'Profile updated successfully')
        return redirect('profile', author=author) 

    context = {
        'form':form, 
        'profile': profile
    }
    
    return render(request, 'edit_profile.html', context)


@login_required
def delete_ques(request, slug):
    question = Question.objects.get(slug=slug)
    author = question.author
    print(author)
    question.delete()
    messages.info(request, 'Question deleted')
    return redirect('profile', author=author)


@login_required
def edit_ques(request, slug):
    question = Question.objects.get(slug=slug)
    if request.method == 'GET':
        title = question.title
        body = question.body
        tags = question.tags.all()
        context = {
            'title': title,
            'body': body,
            'tags': tags
        }
        return render(request, 'ask.html', context)
    else:
        title = request.POST['title']
        body = request.POST['body']
        tags = request.POST['tags']
        question.tags.set('')
        question.title = title
        question.body = body
        question.save()
        all_tags = tags.split()
        for tag in all_tags:
            try:
                tag = Tags.objects.get(tag_word=tag)
                question.tags.add(tag)
            except Exception:
                question.tags.create(tag_word=tag)
            question.save()
        messages.success(request, 'Question Updated')
        return redirect('question', slug=question.slug)


@login_required
def edit_ans(request, id):
    answer = Answer.objects.get(id=id)
    question = answer.question_to_ans
    ques_votes = Questionvote.objects.filter(question=question).count()
    slug = question.slug

    if request.method == 'GET':
        form = AnswerForm(instance=answer)
    else:
        form = AnswerForm(request.POST, instance=answer)
        if form.is_valid():
            form.save()
            return redirect('question', slug=slug)

    context = {
        'form': form,
        'question': question,
        'ques_votes': ques_votes
    }
    
    return render(request, 'edit_answer.html', context)


@login_required
def delete_ans(request, id):
    answer = Answer.objects.get(id=id)
    author = answer.answered_by.username
    answer.delete()
    messages.info(request, 'Answer Deleted')
    return redirect('profile', author=author)
