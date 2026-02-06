import base64
import io
from PIL import Image
from ollama import Client

client = Client(host="http://127.0.0.1:11434")

MODEL_NAME = "qwen3-vl:8b"

SYSTEM_PROMPT = """
You are a highly constrained vision-language image analysis model (LVLM) specialized in group interaction analysis.

***PRIMARY INSTRUCTION:***
Your SOLE job is to analyze the provided image and extract the four required analysis elements below, strictly adhering to the "ANALYSIS RULES" and the "OUTPUT FORMAT (STRICT)".

ANALYSIS ELEMENTS TO EXTRACT:
1. Age composition
2. Spatial formation
3. Postural assessment
4. Focus assessment
5. Engagement rating

ANALYSIS RULES:

RULE 1: DEMOGRAPHIC CLASSIFICATION
- Determine the predominant age composition of the group.
Classification Terms (Select One):
Mixed Adults: (Significant mix of young, middle-aged or senior adults).
Mixed People: (Significant mix of adolescents and adults)
Kids: (Majority appear 2-10 years old)
Adolescents: (Majority appear 10-18 years old).
Primarily Young Adults: (Majority appear 18-35 years old).
Primarily Middle-Aged: (Majority appear 35-65 years old).
Seniors/Older Adults: (Majority appear 65+ years old).

RULE 2: SPATIAL FORMATION ANALYSIS
- Determine the primary arrangement of the individuals in the space.
Classification Terms (Select One):
Arc/Semicircle: People are facing a central point (guide/robot).
Linear/Row: People are standing/sitting in a straight line or two parallel rows.
Dense Cluster: People are tightly grouped with no obvious direction or focus.
Staged/Posed: A formal arrangement clearly set up for a photograph.
Dispersed/Scattered: Individuals are spread loosely throughout the space.

RULE 3: POSTURAL ASSESSMENT
- Determine the dominant physical state of the group.
Classification Terms (Select One):
Standing Only: All visible people are standing upright.
Mixed (Standing/Seated): A clear mix of standing and sitting (on chairs, benches, or in wheelchairs).
Primarily Seated: All visible people are sitting.
dbek_cvsp

RULE 4: FOCUS ASSESSMENT
- Assess the gaze direction.
Classification Terms (Select One):
Focused on Exhibit/Guide: (90-100%) of visible individuals have their heads/eyes directed toward the camera (if the camera represents the guide).
Most Focused on Exhibit/Guide: The majority of the people (51-89%) are looking at the target, but a few are distracted or looking at peers.
Mixed Focus: A clear split (roughly 50/50) between those looking to the target and those looking elsewhere.
Looking Elsewhere:  Most individuals are looking up, down, at their phones, or at each other rather than the exhibit.

RULE 5: ENGAGEMENT RATING
Task: Evaluate the collective interaction of the group with the exhibition or guide. Observation Points: Eye gaze, head orientation, body "lean," and use of mobile devices.
Classification Categories (Select One):
High Engagement: (90%+) of the group is physically oriented toward the exhibit or guide. Heads are up, eyes are forward, and bodies are often leaning slightly toward the target. Minimal to no phone usage.
Moderate Engagement: The majority (above 50%) are focused, but there are clear "pockets" of distraction. Some people are talking to each other, looking at the floor, or checking a device, but the primary group formation still faces the guide/exhibit.
Low Engagement: * Criteria: Less than (50%) are focused on the intended target. Many people have their backs turned, are looking at their phones, or are focused entirely on their peers/environment rather than the exhibition.
Passive/Observation Only: The group is present but shows no active visual or physical "reach" toward the target. Blank expressions, "wandering" eyes, or relaxed/slumped postures that suggest they are waiting rather than participating.

OUTPUT FORMAT (STRICT):
**DO NOT INCLUDE ANY TEXT, MARKDOWN, OR EXPLANATION OUTSIDE OF THIS JSON BLOCK.**
**YOU MUST USE THE EXACT KEY NAMES PROVIDED.**
```json
{
  "Age composition": "Select from Rule 1",
  "Spatial formation": "Select from Rule 2",
  "Postural assessment": "Select from Rule 3",
  "Focus assessment": "Select from Rule 4",
  "Engagement rating": "Select from Rule 5"
}
"""


def encode_image_to_base64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")


def generate(payload):
    text = payload["message"]["text"]
    image_path = payload["message"]["files"][0]
    img_b64 = encode_image_to_base64(image_path)

    response = client.chat(
        model=MODEL_NAME,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": text, "images": [img_b64]}
        ]
    )

    return response.message.content

