# Django 2.0 url import
from django.urls import include, path

#regular expressions
# the r in r'^cts/index.html$' indicates that what is inside the quotes is a regular expression
# the ^ in r'^cts/index.html$' indicates that we are looking to extend from the root dir from this part of the string
# the $ in r'^cts/index.html$' indicates that we are looking to extend end the mathing part exactly here

print('qed.urls')
#appends to the list of url patterns to check against
urlpatterns = [
    ##django 1.X
	#url(r'^', include('splash_app.urls')),
    #url(r'^pram', include('pram_app.urls')),
    #django 2.X
    path('', include('splash_app.urls')),
    path('pram/', include('pram_app.urls')),
    path('nta/', include('nta_app.urls')),
]


handler404 = 'splash_app.views.landing.page_404'
handler500 = 'splash_app.views.landing.page_404'
handler403 = 'splash_app.views.landing.page_404'