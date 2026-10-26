from django.http import HttpResponse


def home(request):
    html = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
      <meta charset="UTF-8">
      <title>Healthcare Backend API</title>
      <style>
        body { font-family: Arial, sans-serif; max-width: 720px; margin: 60px auto; padding: 0 20px; color: #222; }
        h1 { color: #0b6e4f; }
        code { background: #f2f2f2; padding: 2px 6px; border-radius: 4px; }
        table { border-collapse: collapse; width: 100%; margin-top: 16px; }
        th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
        th { background: #f7f7f7; }
      </style>
    </head>
    <body>
      <h1>Healthcare Backend API</h1>
      <p>Status: <strong>running</strong>. Authenticate with JWT:
         <code>Authorization: Bearer &lt;access_token&gt;</code></p>
      <table>
        <tr><th>Resource</th><th>Endpoint</th></tr>
        <tr><td>Register</td><td><code>POST /api/auth/register/</code></td></tr>
        <tr><td>Login</td><td><code>POST /api/auth/login/</code></td></tr>
        <tr><td>Patients</td><td><code>/api/patients/</code></td></tr>
        <tr><td>Doctors</td><td><code>/api/doctors/</code></td></tr>
        <tr><td>Mappings</td><td><code>/api/mappings/</code></td></tr>
      </table>
    </body>
    </html>
    """
    return HttpResponse(html)