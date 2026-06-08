import google.auth

credentials, project = google.auth.default()

print(type(credentials))
print(project)
