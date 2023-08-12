# DocuQuery

### Description
DocuQuery is a web application designed to revolutionize how users interact with documents. It enables users to upload PDF files and then ask questions about the content of those files. Leveraging state-of-the-art NLP techniques and embeddings, DocuQuery seeks to provide accurate and context-aware answers to user queries.

### Features
- User-friendly Interface: Simple and intuitive UI that facilitates file uploads and querying.
- PDF Processing: Ability to upload and process PDF files, extracting their textual content for further analysis.
- Advanced Question-Answering System: Uses embeddings, text splitting, and other advanced NLP techniques to answer user queries based on the content of the uploaded document.
- Secure File Handling: Implements secure file handling mechanisms to ensure user data safety.

### Technical Details

#### Libraries and Frameworks
- PyPDF2: Extracts text from uploaded PDFs.
- LangChain: A library that facilitates embeddings, text splitting, and question-answering. It acts as a middleman between OpenAI LLM and your documents
- OpenAI GPT-4 LLM: Provides embeddings and other potential NLP functionalities.
- Flask: Web application framework used for backend development.

#### Configuration
- File Storage: A dedicated directory, user_files, is used to securely store user-uploaded files.
- Supported File Types: Currently, only PDF files are supported for uploads.

### How to Use
- Clone the Repository: Start by cloning the repository to your local machine.
- Install Required Packages: Ensure you have all the required packages and libraries installed.
- Set Up Configuration:
    - Copy the config_template.py file and rename the copy to config.py.
    - Copy code:
    - `cp config_template.py config.py`
    - Open config.py and replace 'your_api_key_here' with your actual OpenAI API key.
- Running the App: Execute main.py to launch the application.
    - `python main.py`

Usage:

If the application has a web interface, navigate to the provided localhost URL in your browser.
Use the features provided by the application as per the documentation.
Note:
Ensure you never commit the config.py file with your actual API key. The .gitignore file has been set up to ignore this file, but always be cautious when committing changes.
