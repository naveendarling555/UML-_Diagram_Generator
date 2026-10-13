# UML Studio AI — Text to UML Diagram Generator

A beginner-friendly Flask web app that turns a software description into five UML-style diagrams:
- Class diagram
- Use-case diagram
- Sequence diagram
- Activity diagram
- State diagram

## Requirements
- Python 3.10 or newer
- Internet connection in the browser for Mermaid diagram rendering (CDN)

## Windows setup
1. Extract `UML_Studio_AI.zip`.
2. Open the extracted `UML_Studio_AI` folder.
3. Click the address bar in File Explorer, type `cmd`, and press Enter.
4. Run:

```bash
py -m venv .venv
.venv\Scripts\activate
py -m pip install -r requirements.txt
py app.py
```

5. Open `http://127.0.0.1:5000` in Chrome or Edge.
6. Paste a description and click **Generate diagrams**.

## Example description
A Student Management System allows students to register, log in, search courses, and view their results. The admin manages student details and generates reports. Each student has a name, email, phone, and status. The system contains courses and uses notifications to inform students.

## Project workflow
1. User enters natural-language requirements.
2. Text is cleaned and searched for domain concepts.
3. Action words are mapped to candidate methods/use cases.
4. Relationship cues are identified.
5. Mermaid syntax is generated and visualized in the browser.

## Important project limitation
This is an educational NLP-inspired prototype using transparent rules and keyword matching. It does not understand every sentence like a large language model, and generated UML should be reviewed before real software design use.

## Folder structure
```text
UML_Studio_AI/
├── app.py
├── uml_engine.py
├── requirements.txt
├── README.md
├── templates/
│   └── index.html
└── static/
    ├── style.css
    └── app.js
```

## Submission checklist
- [ ] Run the application locally
- [ ] Generate diagrams from at least three different descriptions
- [ ] Capture screenshots of each diagram
- [ ] Record a short demo showing input, generation, and diagram tabs
- [ ] Add your name, college, and guide details to your report if required
- [ ] Upload the folder to GitHub

## Suggested report sections
Abstract, problem statement, objectives, existing vs proposed system, system architecture, NLP extraction workflow, implementation, testing, screenshots, limitations, future enhancement, conclusion, references.
