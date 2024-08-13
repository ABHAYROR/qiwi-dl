# functions/index.py
from urllib.parse import urlparse, parse_qs
import js
from pyodide.http import pyfetch
from bs4 import BeautifulSoup

async def handle_request(request):
    if request.method == "POST":
        form_data = await request.form()
        url = form_data.get('url')
        if not url:
            return js.Response.json({"error": "No URL provided"}, status=400)
        
        try:
            response = await pyfetch(url)
            text = await response.string()
            soup = BeautifulSoup(text, 'html.parser')
            ext = soup.find('h1').text.split('.')[-1] if soup.find('h1') else 'html'
            
            domain = 'https://spyderrock.com/'
            file_id = url.split('/file/')[1]
            new_url = f"{domain}{file_id}.{ext}"
            
            return js.Response.redirect(new_url, status=302)
        except Exception as e:
            return js.Response.json({"error": str(e)}, status=500)
    else:
        html = """
        <!DOCTYPE html>
        <html>
        <body>
            <form action="/" method="post">
                <label for="url">Enter link:</label>
                <input type="text" id="url" name="url" required>
                <input type="submit" value="Submit">
            </form>
        </body>
        </html>
        """
        return js.Response(html, headers={"Content-Type": "text/html"})

async def onRequest(context):
    return await handle_request(context.request)
