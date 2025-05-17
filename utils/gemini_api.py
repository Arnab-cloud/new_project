import json
import logging
import requests
from typing import Dict, Any, List
from google import genai

logger = logging.getLogger(__name__)

def call_gemini_api(prompt: str, api_key: str) -> Dict[str, Any]:
    """
    Make a request to the Google Gemini API
    
    Args:
        prompt (str): The prompt text to send to the API
        api_key (str): Gemini API key
        
    Returns:
        Dict[str, Any]: JSON response from the API
    """
    try:
        # Due to API limitations, we're providing mock responses for demonstration
        logger.info(f"Processing prompt: {prompt[:50]}...")
        
        client = genai.Client(api_key=api_key)
        response = client.models.generate_content (
            model="gemini-2.0-flash",
            contents=prompt
        )

        return response
        # Create a structured mock response based on the prompt context
        # if "resume" in prompt.lower():
        #     return {
        #         "candidates": [
        #             {
        #                 "output": """
        #                 {
        #                   "extracted_skills": ["Python", "JavaScript", "React", "Flask", "SQL", "AWS", "Git"],
        #                   "matching_skills": ["Python", "JavaScript", "React", "SQL"],
        #                   "missing_skills": ["Docker", "CI/CD", "Agile"],
        #                   "experience_summary": "3 years of software development experience with focus on web applications",
        #                   "education_summary": "Bachelor's degree in Computer Science",
        #                   "match_score": 78,
        #                   "strengths": ["Strong frontend skills", "Good database knowledge", "Problem-solving abilities"],
        #                   "weaknesses": ["Limited DevOps experience", "No cloud certification", "Needs more team leadership experience"],
        #                   "overall_assessment": "Good candidate with solid technical skills matching most requirements. Some gaps in DevOps and cloud experience that may require training."
        #                 }
        #                 """
        #             }
        #         ]
        #     }
        # elif "feedback" in prompt.lower() or "sentiment" in prompt.lower():
        #     return {
        #         "candidates": [
        #             {
        #                 "output": """
        #                 {
        #                   "sentiment_score": 0.25,
        #                   "primary_sentiment": "Mixed",
        #                   "key_themes": ["Work-life balance", "Team collaboration", "Career growth", "Compensation"],
        #                   "positive_aspects": ["Supportive team environment", "Interesting projects", "Learning opportunities"],
        #                   "concerns": ["High workload", "Limited advancement opportunities", "Communication issues with management"],
        #                   "attrition_risk": {
        #                     "level": "medium",
        #                     "reasoning": "Employee shows signs of dissatisfaction with growth opportunities and workload, but appreciates team and projects"
        #                   },
        #                   "engagement_recommendations": ["Address work-life balance concerns", "Provide clearer career path", "Improve management communication", "Consider compensation review"],
        #                   "summary": "Employee shows mixed satisfaction levels with positive feelings toward team and work content but concerns about workload and advancement."
        #                 }
        #                 """
        #             }
        #         ]
        #     }
        # else:
        #     return {
        #         "candidates": [
        #             {
        #                 "output": "Could not parse the request type. Please specify either resume analysis or sentiment analysis."
        #             }
        #         ]
        #     }
        
    except requests.exceptions.RequestException as e:
        logger.error(f"API request error: {str(e)}")
        raise Exception(f"Failed to call Gemini API: {str(e)}")
    except json.JSONDecodeError as e:
        logger.error(f"JSON decode error: {str(e)}")
        raise Exception(f"Failed to parse API response: {str(e)}")

def analyze_resume_with_gemini(resume_text: str, job_description: str, api_key: str) -> Dict[str, Any]:
    """
    Analyze resume text against job description using Gemini API
    
    Args:
        resume_text (str): Extracted text from resume
        job_description (str): Job description text
        api_key (str): Gemini API key
        
    Returns:
        Dict[str, Any]: Structured analysis result
    """
    try:
        prompt = f"""
        You are an expert HR recruiter specializing in tech roles. Analyze the resume below for a Software Engineer position.
        
        JOB DESCRIPTION:
        {job_description}
        
        RESUME:
        {resume_text}
        
        Provide a JSON response with the following structure:
        1. extracted_skills (array): List of technical skills found in the resume
        2. matching_skills (array): Skills from the resume that match the job description
        3. missing_skills (array): Important skills mentioned in the job description but missing from the resume
        4. experience_summary (string): Brief summary of the candidate's relevant experience
        5. education_summary (string): Brief summary of the candidate's education
        6. match_score (number): A score from 0-100 indicating how well the resume matches the job description
        7. strengths (array): Key strengths of the candidate
        8. weaknesses (array): Areas where the candidate may need improvement
        9. overall_assessment (string): A brief overall assessment of the candidate's fit for the role
        
        Format your response as a valid JSON object with these keys.
        """
        
        response = call_gemini_api(prompt, api_key)
        print(response.text)
        result = json.loads(response.text.strip('`').lstrip('json\n'))
        return result
        # Extract the JSON from the response
        # text_response = response['candidates'][0]['output']
        
        # Find JSON content (between curly braces)
        # json_start = text_response.find('{')
        # json_end = text_response.rfind('}') + 1
        
        # if json_start >= 0 and json_end > json_start:
        #     json_str = text_response[json_start:json_end]
        #     return json.loads(json_str)
        # else:
        #     # If JSON parsing fails, create a structured response from the text
        #     logger.warning("Could not extract JSON from API response, creating structured response")
        #     return {
        #         "extracted_skills": [],
        #         "matching_skills": [],
        #         "missing_skills": [],
        #         "experience_summary": "Could not extract experience summary",
        #         "education_summary": "Could not extract education summary",
        #         "match_score": 0,
        #         "strengths": [],
        #         "weaknesses": [],
        #         "overall_assessment": text_response
        #     }
            
    except Exception as e:
        logger.error(f"Resume analysis error: {str(e)}")
        raise Exception(f"Failed to analyze resume: {str(e)}")

def analyze_sentiment_with_gemini(feedback_text: str, api_key: str) -> Dict[str, Any]:
    """
    Analyze employee feedback for sentiment using Gemini API
    
    Args:
        feedback_text (str): Employee feedback text
        api_key (str): Gemini API key
        
    Returns:
        Dict[str, Any]: Structured sentiment analysis result
    """
    try:
        prompt = f"""
        You are an expert HR analyst specializing in employee engagement and retention. Analyze the following employee feedback text:
        
        EMPLOYEE FEEDBACK:
        {feedback_text}
        
        Provide a JSON response with the following structure:
        1. sentiment_score (number): Overall sentiment score from -1.0 (very negative) to 1.0 (very positive)
        2. primary_sentiment (string): The primary sentiment detected (e.g., "positive", "negative", "neutral", "mixed")
        3. key_themes (array): List of key themes/topics identified in the feedback
        4. positive_aspects (array): Positive aspects mentioned in the feedback
        5. concerns (array): Concerns or issues mentioned in the feedback
        6. attrition_risk (object): 
           - level (string): Risk level ("low", "medium", "high")
           - reasoning (string): Brief explanation for the risk assessment
        7. engagement_recommendations (array): Specific recommendations to improve engagement based on the feedback
        8. summary (string): Brief summary of the feedback analysis
        
        Format your response as a valid JSON object with these keys.
        """
        
        response = call_gemini_api(prompt, api_key)

        return json.loads(response.text.strip('`').lstrip('json\n'))
        
        # # Extract the JSON from the response
        # text_response = response['candidates'][0]['output']
        
        # # Find JSON content (between curly braces)
        # json_start = text_response.find('{')
        # json_end = text_response.rfind('}') + 1
        
        # if json_start >= 0 and json_end > json_start:
        #     json_str = text_response[json_start:json_end]
        #     return json.loads(json_str)
        # else:
        #     # If JSON parsing fails, create a structured response from the text
        #     logger.warning("Could not extract JSON from API response, creating structured response")
        #     return {
        #         "sentiment_score": 0,
        #         "primary_sentiment": "unknown",
        #         "key_themes": [],
        #         "positive_aspects": [],
        #         "concerns": [],
        #         "attrition_risk": {
        #             "level": "unknown",
        #             "reasoning": "Could not determine risk level"
        #         },
        #         "engagement_recommendations": [],
        #         "summary": text_response
        #     }
            
    except Exception as e:
        logger.error(f"Sentiment analysis error: {str(e)}")
        raise Exception(f"Failed to analyze sentiment: {str(e)}")
