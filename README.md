# Nirmaanify Website

This is the main website for Nirmaanify, a tech startup based in India. We built this to handle client inquiries, service requests, and internship applications.

## What it does

The website serves as our main business presence with:
- Company information and services overview
- Contact forms for potential clients
- Service request forms for project inquiries  
- Internship application system for students
- Admin dashboard to manage all submissions

## Getting it running

Make sure you have Python 3.7+ installed, then:

```bash
# Install the required packages
pip install -r requirements.txt

# Start the server
python app.py
```

The site will be available at http://localhost:5000

## Project structure

```
nirmaanify/
├── app.py                    # Main Flask application
├── controllers/              # API endpoints for forms
│   ├── contact_controller.py
│   ├── services_controller.py  
│   └── training_controller.py
├── data/
│   └── submissions.json      # Where form data gets stored
├── *.html                    # Website pages
├── style.css                 # All the styling
├── script.js                 # Frontend functionality
└── requirements.txt          # Python dependencies
```

## API stuff

The backend handles these endpoints:

**Contact forms:**
- `POST /api/contact` - Submit contact form
- `GET /api/contact` - Get all contact submissions

**Service requests:**
- `POST /api/services` - Submit service request  
- `GET /api/services` - View all service requests
- `GET /api/services/stats` - Get some basic stats

**Internship applications:**
- `POST /api/training` - Submit internship application
- `GET /api/training` - View all applications
- `GET /api/training/stats` - Get application stats

**General:**
- `GET /api/health` - Check if server is running
- `GET /api/submissions` - View everything (admin use)

## Admin access

There's a simple admin dashboard at `/admin.html` with password protection. Default password is `nirmaanvr01` (you should change this in production).

The dashboard shows:
- Total submission counts
- Recent form submissions
- Basic statistics

## Data storage

Right now we're using JSON file storage in `data/submissions.json`. It's simple and works fine for our current needs. Each submission gets a unique ID and timestamp.

The data structure looks like this:
```json
{
  "contacts": [
    {
      "id": "contact_20250101_120000",
      "type": "contact",
      "timestamp": "2025-01-01T12:00:00", 
      "data": {
        "name": "John Doe",
        "email": "john@example.com",
        "subject": "General Inquiry",
        "message": "Hello, I have a question..."
      }
    }
  ],
  "services": [],
  "internships": []
}
```

## Customization

**Adding new forms:**
1. Create a new controller in the `controllers/` folder
2. Add the blueprint to `app.py`
3. Update the data structure in the controller
4. Modify the admin dashboard if needed

**Styling:**
- Everything is in `style.css`
- We're using a purple theme (#6A3EE8)
- It's responsive and works on mobile

**Frontend:**
- Form handling is in `script.js`
- Includes mobile menu, animations, and notifications
- All forms have validation

## Deployment notes

For production, you'll want to:

1. **Replace JSON storage with a real database** (PostgreSQL or MySQL)
2. **Set proper environment variables** for secrets
3. **Use a WSGI server** like Gunicorn
4. **Set up a reverse proxy** with Nginx
5. **Enable HTTPS**

The current setup is fine for development but not production-ready.

## Common issues

**Port already in use:**
```bash
lsof -i :5000
kill -9 <PID>
```

**Forms not submitting:**
- Check if the Flask server is running
- Look at browser console for JavaScript errors
- Make sure the `data/` folder has write permissions

**Admin dashboard not working:**
- Clear browser cache
- Check if JavaScript is enabled
- Verify the password is correct

## Dependencies

- Flask 2.3.3 - Web framework
- Flask-CORS 4.0.0 - Cross-origin requests
- Werkzeug 2.3.7 - WSGI utilities

## Future improvements

We're planning to add:
- Database migration (probably PostgreSQL)
- Email notifications when forms are submitted
- Payment processing for certificates
- Better admin authentication
- More detailed analytics

## Contact

Questions about the code? Reach out:
- Email: contact@nirmaanify.com
- Phone: +91-326-6356-5201

---

This project is actively maintained by the Nirmaanify team. If you find any bugs or have suggestions, feel free to let us know!