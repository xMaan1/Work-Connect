from urllib.request import urlretrieve
from django.core.files import File
from tempfile import NamedTemporaryFile

def get_avatar(backend, strategy, details, response, user=None, *args, **kwargs):
    if user:
        if backend.name == 'google-oauth2':
            if response.get('picture'):
                url = response['picture']
            else:
                return
        elif backend.name == 'linkedin-oauth2':
            if response.get('profilePicture'):
                url = response['profilePicture']['displayImage~']['elements'][0]['identifiers'][0]['identifier']
            else:
                return
        else:
            return

        try:
            if hasattr(user, 'jobseekerprofile'):
                profile = user.jobseekerprofile
            elif hasattr(user, 'companyprofile'):
                profile = user.companyprofile
            else:
                return

            if not profile.profile_picture:  # Only update if no picture exists
                img_temp = NamedTemporaryFile(delete=True)
                urlretrieve(url, img_temp.name)
                profile.profile_picture.save(f'{user.username}_social.jpg', File(img_temp))
                profile.save()
        except Exception as e:
            print(f"Error saving profile picture: {str(e)}")
            pass

def clean_username(username):
    """
    Clean the username from the social auth provider.
    Remove any special characters and spaces.
    """
    return username.replace('@', '').replace('.', '_').lower()
