# About Project
The project's sole prupose is to demonstrate the __JWT authentication using Django Rest Framework__. Also this could be a __bouilerplate mini-functionality of bigger projects__, where the Django is used as the backend technology along with any frontend framework.

YT Video Ref: [Django API Authentication using JWT Tokens](https://www.youtube.com/watch?v=PUzgZrS_piQ)

### Signup System
- Create user data using a serializer, in which the password is hashed using default create method of the **ModelSerializer**. Also, prohibit the password being sent alongside the user-detail as a successful response.

### Login System
- Generate JWT token in enevry successful login attempt. Set the token in the client-end using session-cookie.
  - More about **["set_cookie()"]("https://betterprogramming.pub/managing-cookies-in-django-34981d9bf0ae")** method.
<br/>

# Tech stack
- MySQL (_inside docker_)
- Postman (_API testing & debugging_)