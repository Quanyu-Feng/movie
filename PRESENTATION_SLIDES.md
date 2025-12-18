# myMovie Project Presentation
## Complete Slide Content for PowerPoint/Google Slides

---

## Slide 1: Title Slide

**Title:** 🎬 myMovie

**Subtitle:** Modern Full-Stack Movie Discovery Platform

**Description:** A serverless web application for discovering movies and managing your watchlist

**Technology Stack:** Python Serverless Functions + HTML/CSS/JavaScript

---

## Slide 2: Project Overview

### 📋 Project Overview

**myMovie** is a modern, full-stack web application that provides users with:

- 🎥 **Real-time Movie Data** from The Movie Database (TMDB)
- ▶️ **YouTube Trailer Integration** for instant previews
- 👤 **User Authentication** (Register/Login)
- ⭐ **Favorites Management** to save your preferred movies
- 📜 **Watch History Tracking** to remember what you've watched

*Built with a modern serverless architecture for scalability and performance*

---

## Slide 3: Technology Stack

### 🛠️ Technology Stack

#### Frontend
- HTML5
- CSS3
- JavaScript (ES6+)

#### Backend
- Python 3.12
- Serverless Functions
- HTTP Request Handler

#### Database
- PostgreSQL
- Supabase

#### Deployment
- Vercel
- GitHub
- CI/CD

---

## Slide 4: Key Features - Part 1

### ✨ Key Features

#### 🎬 Movie Discovery
- Browse trending movies
- Search by title
- Filter by genre
- View detailed information
- Real-time data from TMDB API

#### 👤 User Management
- Secure registration
- Password encryption
- Session management
- Profile persistence

---

## Slide 5: Key Features - Part 2

### ✨ Key Features (Continued)

#### ⭐ Favorites System
- Add movies to favorites
- Remove from favorites
- View all saved movies
- Persistent storage

#### 📜 Watch History
- Auto-track watched movies
- View watching history
- Clear history option
- Chronological ordering

---

## Slide 6: System Architecture

### 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                         Frontend                            │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐  │
│  │  HTML    │  │   CSS    │  │JavaScript│  │  TMDB    │  │
│  │  Pages   │  │  Styles  │  │   Logic  │  │   API    │  │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘  │
└─────────────────────────────────────────────────────────────┘
                            ↓ HTTP/HTTPS
┌─────────────────────────────────────────────────────────────┐
│                    Vercel Platform                          │
│  ┌──────────────────────────────────────────────────────┐  │
│  │         Serverless Functions (Python)                │  │
│  │  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌─────────┐│  │
│  │  │  login   │ │ register │ │favorites │ │ history ││  │
│  │  │   .py    │ │   .py    │ │   .py    │ │   .py   ││  │
│  │  └──────────┘ └──────────┘ └──────────┘ └─────────┘│  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                            ↓ Database Connection
┌─────────────────────────────────────────────────────────────┐
│                  Database (Supabase)                        │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐                 │
│  │  Users   │  │Favorites │  │ History  │                 │
│  │  Table   │  │  Table   │  │  Table   │                 │
│  └──────────┘  └──────────┘  └──────────┘                 │
└─────────────────────────────────────────────────────────────┘
```

---

## Slide 7: Frontend Technology

### 🎨 Frontend Technology

**Pure HTML/CSS/JavaScript - No Framework Dependencies**

#### Responsive Design
- Mobile-first approach
- Flexible grid layouts
- Media queries for all screen sizes

#### Modern JavaScript (ES6+)
- Async/Await for API calls
- Module pattern for organization
- LocalStorage for session management

#### External API Integration
- TMDB API for movie data
- YouTube API for trailers

---

## Slide 8: Backend Technology

### ⚙️ Backend Technology

**Python Serverless Functions**

#### Architecture Benefits:
- ✅ Auto-scaling
- ✅ Pay-per-use pricing
- ✅ Zero server maintenance
- ✅ Global edge deployment
- ✅ Built-in SSL/HTTPS

#### API Endpoints:
- `POST /api/login`
- `POST /api/register`
- `GET/POST/DELETE /api/favorites`
- `GET/POST/DELETE /api/history`

**Security:** Password hashing with Werkzeug, CORS enabled, SQL injection protection

---

## Slide 9: Database Design

### 🗄️ Database Design

**PostgreSQL Schema (Supabase)**

#### Users Table:
| Column     | Type         | Description |
|------------|--------------|-------------|
| id         | SERIAL PK    | User ID     |
| username   | VARCHAR(50)  | Unique name |
| password   | VARCHAR(255) | Hashed pwd  |
| created_at | TIMESTAMP    | Join date   |

#### Favorites Table:
| Column       | Type         | Description |
|--------------|--------------|-------------|
| id           | SERIAL PK    | Record ID   |
| user_id      | INTEGER FK   | User ref    |
| movie_id     | INTEGER      | TMDB ID     |
| movie_title  | VARCHAR(255) | Title       |
| poster_path  | VARCHAR(255) | Image URL   |
| added_at     | TIMESTAMP    | Add time    |

#### History Table:
| Column      | Type         | Description |
|-------------|--------------|-------------|
| id          | SERIAL PK    | Record ID   |
| user_id     | INTEGER FK   | User ref    |
| movie_id    | INTEGER      | TMDB ID     |
| video_key   | VARCHAR(50)  | YouTube key |
| watched_at  | TIMESTAMP    | Watch time  |

---

## Slide 10: Deployment & CI/CD

### 🚀 Deployment & CI/CD

**Automated Deployment with Vercel**

#### Workflow:

1. **Development**
   - Code changes pushed to GitHub
   - Version control with Git

2. **Automatic Build**
   - Vercel detects GitHub push
   - Builds Python functions
   - Optimizes static assets

3. **Deployment**
   - Deploy to global CDN
   - Environment variables configured
   - Instant live updates

4. **Monitoring**
   - Real-time logs
   - Performance analytics
   - Error tracking

---

## Slide 11: Code Example - Backend

### 💻 Code Highlights

**Python Serverless Function Example**

```python
from http.server import BaseHTTPRequestHandler
import json
from _db import get_db

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        # Read request body
        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length).decode('utf-8')
        data = json.loads(body)
        
        # Process request
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE username = %s', 
                      (data['username'],))
        user = cursor.fetchone()
        
        # Send JSON response
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps({'success': True}).encode('utf-8'))
```

---

## Slide 12: Code Example - Frontend

### 💻 Code Highlights

**Frontend API Integration Example**

```javascript
// Login function with async/await
const tryLogin = async function (event) {
    event.preventDefault();
    
    try {
        const response = await fetch('/api/login', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                username: username.value,
                password: password.value
            })
        });
        
        const data = await response.json();
        
        if (data.success) {
            // Save user session
            localStorage.setItem('isLoggedIn', 'true');
            localStorage.setItem('userId', data.user_id);
            window.location.href = './index.html';
        }
    } catch (error) {
        console.error('Login error:', error);
    }
}
```

---

## Slide 13: Performance & Scalability

### ⚡ Performance & Scalability

#### Performance
- ✅ **Fast Load Times**
  - Optimized assets
  - CDN delivery
- ✅ **Efficient API**
  - Minimal database queries
  - Connection pooling
- ✅ **Caching Strategy**
  - LocalStorage for sessions
  - Browser caching

#### Scalability
- ✅ **Serverless Architecture**
  - Auto-scaling
  - No capacity planning
- ✅ **Global Distribution**
  - Edge network
  - Low latency worldwide
- ✅ **Database Optimization**
  - Indexed queries
  - Efficient schema

---

## Slide 14: Security Features

### 🔒 Security Features

#### 🔐 Password Security
- Werkzeug password hashing (PBKDF2)
- Salted hashes for each user
- No plaintext password storage

#### 🛡️ SQL Injection Protection
- Parameterized queries
- psycopg2 prepared statements

#### 🌐 CORS Configuration
- Proper CORS headers
- OPTIONS preflight handling

#### 🔑 Environment Variables
- Sensitive data not in code
- Secure database connection strings

---

## Slide 15: Future Enhancements

### 🚀 Future Enhancements

#### Features
- 🎯 Personalized recommendations
- 👥 Social features (share favorites)
- 📊 User statistics dashboard
- 🔔 New release notifications
- ⭐ Movie ratings & reviews
- 🎭 Actor/Director pages

#### Technical
- 🔍 Advanced search filters
- 📱 Progressive Web App (PWA)
- 🌙 Dark/Light theme toggle
- 🌍 Multi-language support
- 📧 Email verification
- 🔄 OAuth integration

---

## Slide 16: Lessons Learned

### 📚 Lessons Learned

#### Serverless Advantages
- Simplified deployment and scaling
- Cost-effective for variable traffic
- Quick iteration and updates

#### API Design
- Importance of proper error handling
- RESTful principles for clarity
- CORS configuration essentials

#### Frontend Architecture
- Vanilla JS can be powerful and fast
- LocalStorage for simple state management
- Progressive enhancement approach

---

## Slide 17: Live Demo

### 📸 Live Demo

**Visit the Application**

**🌐 URL:**
[movie-git-main-quanyu-fengs-projects.vercel.app](https://movie-git-main-quanyu-fengs-projects.vercel.app)

**Key Pages to Explore:**
- 🏠 Home - Browse trending movies
- 🔍 Search - Find specific movies
- 👤 Login/Register - User authentication
- ⭐ Favorites - Your saved movies
- 📜 History - Watch tracking

---

## Slide 18: Project Statistics

### 📊 Project Statistics

#### Code
- 📄 7 HTML pages
- 🎨 1,126 lines of CSS
- 💻 12 JavaScript modules
- 🐍 4 Python API functions

#### Features
- 🔌 4 API endpoints
- 🗄️ 3 database tables
- 📡 2 external API integrations
- 🎬 1000s of movies available

#### Infrastructure
- ☁️ Serverless deployment
- 🌍 Global CDN
- 🔄 Auto CI/CD
- ⚡ Sub-second response times

---

## Slide 19: Conclusion

### 🎯 Conclusion

**Why myMovie Succeeds**

- **🎨 Modern UX**
  - Clean, intuitive interface
  - Responsive across all devices

- **⚡ High Performance**
  - Fast load times with serverless architecture
  - Efficient API design

- **📈 Scalable**
  - Auto-scaling infrastructure
  - Ready for growth

- **🔒 Secure**
  - Industry-standard encryption
  - Protected against common vulnerabilities

- **🚀 Easy to Deploy**
  - One-click deployment
  - Automated CI/CD pipeline

---

## Slide 20: Thank You

### Thank You! 🙏

**Questions?**

**Project Links:**

🌐 **Live Demo:**
[movie-git-main-quanyu-fengs-projects.vercel.app](https://movie-git-main-quanyu-fengs-projects.vercel.app)

💻 **GitHub:**
[github.com/Quanyu-Feng/movie](https://github.com/Quanyu-Feng/movie)

*Built with ❤️ using Python, JavaScript, and Vercel*

---

## Instructions for Use

### Option 1: View HTML Presentation
1. Open `presentation.html` in your browser
2. Use arrow keys or click to navigate slides
3. Press 'F' for fullscreen
4. Press 'S' for speaker notes
5. Press 'O' for overview mode
6. Press '?' for help

### Option 2: Import to PowerPoint/Google Slides
1. Open this Markdown file
2. Copy the content for each slide
3. Paste into your presentation tool
4. Add visual elements and adjust formatting
5. Consider adding screenshots of your live application

### Tips for PowerPoint
- Use a dark theme for better contrast
- Add screenshots from your live site
- Include animations for bullet points
- Use consistent font sizes (Title: 44pt, Body: 28pt)
- Add your logo or branding
- Consider printing as PDF for sharing

### Recommended Images to Add
- Homepage screenshot
- Login/Register page
- Movie detail page with trailer
- Favorites list
- Watch history page
- Mobile responsive view
- Architecture diagram (enhance the ASCII art)

