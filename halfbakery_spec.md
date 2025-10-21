# Half-Bakery Project Specification

## Overview
A simple Flask-based project idea repository for classroom use. Students can post "half-baked" project ideas and comment on them with flat chronological threading.

## Target Environment
- Local Raspberry Pi deployment
- Accessible via local network (host='0.0.0.0')
- Python 3 with Flask and Flask-SQLAlchemy
- SQLite database
- No authentication required (educational tool)

## Database Schema

### Projects Table
- `id` (Integer, Primary Key)
- `title` (String, 200 chars)
- `filepath` (String) - path to .md or .txt file containing project description
- `created_at` (DateTime)
- `author_name` (String, 100 chars) - plain text, not a foreign key

### Comments Table
- `id` (Integer, Primary Key)
- `project_id` (Integer, Foreign Key → projects.id)
- `student_name` (String, 100 chars) - plain text, not a foreign key
- `comment_text` (Text)
- `parent_comment_id` (Integer, Foreign Key → comments.id, nullable)
- `quoted_text` (Text, nullable) - snippet from parent comment for display
- `created_at` (DateTime)

## File Storage
- Project descriptions stored as individual files (markdown or text)
- Files stored in a `projects/` directory
- Filenames can be: `project_<id>.md` or similar convention
- Database stores only the filepath, not the content
- Flask reads file content when rendering the project page

## Routes

### `GET /`
- Home page listing all projects
- Display: project title, author, creation date
- Link to each project page

### `GET /projects/<project_id>`
- Display single project page
- Read and render project description from file
- Show all comments in chronological order (flat list)
- Display quoted text in styled box if comment has parent_comment_id
- Include comment form at bottom

### `POST /projects/<project_id>/comment`
- Add new comment to project
- Form fields:
  - `student_name` (required)
  - `comment_text` (required)
  - `parent_comment_id` (optional)
  - `quoted_text` (optional)
- Redirect back to project page after submission

### `GET /projects/new`
- Form to create new project
- Fields:
  - `title` (required)
  - `author_name` (required)
  - `description` (textarea, required)
- On submit: create project record, write description to file

### `POST /projects/create`
- Handle new project creation
- Create database entry
- Write description to file in `projects/` directory
- Redirect to new project page

## UI/UX Requirements

### Comment Display (Chronological Flat Threading)
- All comments display in chronological order (oldest first)
- No visual nesting or indentation
- If comment has `parent_comment_id`:
  - Display quoted text in a distinct style (gray background, smaller font)
  - Show "In reply to [parent author]" or similar
  - Quote appears inline above the comment text

### Comment Reply UI
- Each comment has a "Reply" button/link
- Clicking "Reply" on comment #5:
  - Scrolls to comment form
  - Pre-fills `parent_comment_id` field (hidden)
  - Pre-fills quoted text in a visible "Quoting:" preview box
  - User can edit/trim the quote before submitting
  - User can clear the reply to post a standalone comment

### Styling Inspiration
- Clean, readable typography
- Similar feel to old phpBB/vBulletin forums
- Mobile-friendly basic responsive design
- Minimal JavaScript (enhance progressively if needed)

## Code Style & Organization
- Keep code readable for novice students
- Clear function and variable names
- Comments explaining key concepts
- Separate templates for different pages
- Use Jinja2 template inheritance for consistency

## Error Handling
- 404 for non-existent projects
- Handle missing files gracefully
- Basic form validation
- User-friendly error messages

## Future Enhancements (Not in MVP)
- Edit/delete comments
- User authentication
- Markdown rendering for project descriptions
- Search functionality
- Project tags/categories
- Vote/like system

## Testing Checklist
- [ ] Create a new project
- [ ] View project page
- [ ] Add standalone comment
- [ ] Reply to a comment with quote
- [ ] Verify chronological ordering
- [ ] Check file storage/retrieval
- [ ] Test from multiple devices on local network
- [ ] Verify datetime stamps display correctly