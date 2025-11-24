# MoviWebApp

A full-stack Flask web application for managing users and their favorite movies. Add, update, and delete movies for each user—each film is enriched with real poster, year, and director info fetched from the OMDb API.

**Live Demo:**  
[ledio99.pythonanywhere.com](http://ledio99.pythonanywhere.com/)

## Features

- **User Management:** Easily add and remove users.
- **Movie Lists:** Each user has their own fully editable movie collection.
- **OMDb Integration:** Add movies by title—data (poster, director, year) is pulled from [omdbapi.com](https://www.omdbapi.com/).
- **Edit & Delete:** Update movie details or remove entries with a click.
- **Error Handling:** Clean feedback for missing movies, API errors, or user mistakes.
- **Responsive UI:** Built with Flask, HTML, and CSS for a smooth browser experience.

## Project Structure

MoviWebApp/  
├── app.py # Flask app and routes  
├── data_manager.py # App logic (CRUD and OMDb fetch)  
├── models.py # SQLAlchemy User & Movie models  
├── data/ # SQLite database files  
├── static/ # CSS and static files  
├── templates/ # HTML templates  
├── requirements.txt # Python dependencies

## Setup

1. **Clone this repo:**
```bash
git clone https://github.com/Miami05/MoviWebApp.git
```
```bash
cd MoviWebApp
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Configure environment variables:**
- Register at [OMDb API](https://omdbapi.com/apikey.aspx) for a free API key.
- Add this line to a `.env` file:
  ```
  OMDB_API_KEY=your-omdb-api-key
  ```

4. **Run locally:**
```bash
python app.py
```
- Visit `http://localhost:5002/` in your browser.

## Usage

- **Home:** See all users. Add new users at any time.
- **User Page:** Click a user to view and manage their movies.
- **Add Movie:** Enter any film title—data is auto-filled from OMDb.
- **Update/Delete:** Edit or remove individual movies easily.

## Live Demo

Try the live version here: [ledio99.pythonanywhere.com](http://ledio99.pythonanywhere.com/)

## License

MIT

MoviWebApp is a fun way to organize movie favorites and experiment with web development, APIs, and database integration!
