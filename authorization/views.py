# # Create your views here.
#
#
# def sign_in(request):
#     state, next_page, submissiontype = ('',)*3
#     if request.method == 'POST':
#         try:
#             submissiontype = request.POST.get('submissiontype', 'page')
#             user = CompanyUser.objects.get(email=request.POST['username'])
#             if user.check_password(request.POST['password']):
#                 if user.company:
#                     user.backend = 'mongoengine.django.auth.MongoEngineBackend'
#                     login(request, user)
#                     if submissiontype == 'ajax':
#                         return HttpResponse(
#                             json.dumps({'success': True}),
#                             content_type="application/json"
#                         )
#                     else:
#                         if 'next' in request.POST:
#                             return redirect(request.POST['next'])
#                         return redirect('dashboard.views.dashboard')
#                 else:
#                     state = ("User has an inactive account. Please contact "
#                              "support@eventable.com to reactivate.")
#             else:
#                 state = "Incorrect username/password combination"
#         except DoesNotExist:
#             state = "User does not exist"
#     elif 'next' in request.GET:
#         next_page = request.GET['next']
#     if submissiontype == 'ajax':
#         return HttpResponseBadRequest(
#             json.dumps({'success': False, 'state': state}),
#             content_type="application/json"
#         )
#     else:
#         params = {'state': state, 'next': next_page}
#         return render_to_response(
#             'frontend/login.html', params,
#             context_instance=RequestContext(request)
#         )
#
#
# def logout_user(request):
#     from django.contrib.auth import logout
#     logout(request)
#     return redirect('frontend.views.sign_in')