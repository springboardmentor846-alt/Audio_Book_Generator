AI Audiobook Generator

Project Overview
The AI Audiobook Generator is a Streamlit-based web application that converts text documents into natural-sounding audiobooks using AI-powered text enhancement and neural text-to-speech synthesis.

The system supports multiple file formats and transforms raw content into engaging, narration-ready audio, with optional multilingual conversion and cinematic sound effects integration.

Key Features

1. Multi-Format File Support

* Upload and process: PDF (.pdf), Word (.docx), Text (.txt)
* Automatic text extraction from uploaded files

2. AI-Powered Text Enhancement

* Uses Groq (LLM) to:

  * Convert raw text into audiobook-style narration
  * Improve grammar and flow
  * Break long sentences into natural speech patterns
* Supports narration styles:

  * Professional
  * Storytelling
  * Motivational
  * Podcast Style

3. Multilingual Support

* Converts narration into:

  * English
  * Hindi
  * Marathi
* Maintains tone and storytelling quality across languages

4. Natural Text-to-Speech (TTS)

* Uses Microsoft Edge Neural Voices for high-quality, human-like audio
* Customizations include slower rate and lower pitch for natural sound
* Produces downloadable MP3 audiobook files

5. Cinematic Sound Cue Integration

* Detects expressions inside brackets such as:
  (Sound of birds chirping)
  (Dramatic pause)
  (Soft background music)

* Instead of reading them aloud, the system:

  * Inserts silence for pauses
  * Adds background sound effects
  * Blends audio using pydub

Example

Input Text:
The forest was calm.

(Sound of birds chirping)

He walked slowly.

(Dramatic pause)

Something felt strange.

Output Behavior:

* Bird sound plays instead of reading text
* Silence inserted for pause
* Narration continues smoothly

6. Smart Audio Processing

* Splits long text into smaller chunks
* Generates audio per chunk
* Merges all audio into one seamless file
* Avoids robotic speech

7. Intelligent Processing System

* Chunk-based AI processing to avoid API limits
* Progress bar for user feedback
* Error handling with fallback mechanisms

8. Session State Management

* Maintains extracted text, enhanced text, final text, and audio
* Prevents unnecessary reprocessing

9. Download and Playback

* Built-in audio player
* Download audiobook as MP3

10. Reset Functionality

* Clears all data including text, audio, and session state

System Architecture

Workflow:

Upload File
Text Extraction
Text Cleaning
AI Enhancement (Groq)
Language Translation
Sound Cue Processing
Text-to-Speech (Edge TTS)
Audio Merging (pydub)
Final Audiobook Output

Technologies Used

Frontend UI: Streamlit
AI Text Processing: Groq (LLAMA 3)
PDF Extraction: pdfplumber
DOCX Processing: python-docx
Text Processing: Regex (re module)
Audio Generation: edge-tts
Audio Processing: pydub
Async Processing: asyncio

Sample Input for Testing

The night was calm.

(Sound of gentle wind)

He walked slowly.

(Sound of footsteps)

Suddenly, a noise echoed.

(Dramatic pause)

Something was watching him.

(Suspenseful music)

Key Functional Modules

1. Text Extraction Module

* Extracts content from uploaded files
* Handles multiple formats

2. Text Cleaning Module

* Removes extra spaces and unnecessary formatting
* Normalizes text

3. AI Enhancement Module

* Rewrites text into natural, engaging narration

4. Translation Module

* Converts text into selected language while maintaining tone

5. Sound Cue Processing Module

* Detects bracketed expressions
* Classifies them into pause, sound effects, or music
* Replaces them with actual audio elements

6. Audio Generation Module

* Converts text into speech using TTS

7. Audio Merging Module

* Combines narration and sound effects into final output

Advantages of the Project

* Converts static documents into interactive audio experiences
* Improves accessibility for visually impaired users and multitaskers
* Supports multilingual narration
* Provides cinematic storytelling experience
* Scalable for real-world applications

Limitations

* Requires internet connection for AI processing
* Output quality depends on input text quality
* Background sound library must be managed locally

Future Enhancements

* Voice selection (Male/Female)
* Real-time voice preview
* Background music customization
* Chapter-based audio splitting
* User login and history
* AI-based summarization
* Podcast generation mode
* Deployment as SaaS platform

Conclusion

The AI Audiobook Generator is a modern AI-driven application that combines natural language processing, speech synthesis, and audio engineering to deliver a complete audiobook creation system.

It demonstrates practical use of AI in content transformation, accessibility, and user experience enhancement.

This project has strong potential for academic evaluation, portfolio showcase, and real-world product development.

Author
Om Lonkar 
Infosys Springboard 6.0
Computer Engineering Student

