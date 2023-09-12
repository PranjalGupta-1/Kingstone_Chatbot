#
##
###
#### install all the requirement
##### pip install openai pyttsx3 SpeechRecognition

###### Replace api key
######## Replace avatar location


import openai
import speech_recognition as sr
import pyttsx3
import tkinter as tk
from tkinter import scrolledtext
import threading

# OpenAI API , Replace api key
openai.api_key = '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'

#prompt techniques
prompt_techniques = {
    "role_play": {
        "prompt": """
Role play a scenario where you're a new mother experiencing postpartum anxiety. Act as if you're talking to a supportive friend or family member and seek advice on managing anxiety, maintaining and well-being.

Example Scenario 1:
User: (Role-playing) Friend: Hi! How are you feeling after having a baby?
User: I've been feeling overwhelmed and anxious lately. Can you share any advice on how to cope with postpartum anxiety and take care of myself?

Example Scenario 2:
User: (Role-playing) Sister: I heard you've been struggling with postpartum anxiety. How can I help you?
User: Yes, I've been feeling really anxious lately. Can you give me some tips on managing anxiety and maintaining my well-being as a new mother?
""",
    },
    "chained": {
        "prompt": """
Imagine we previously discussed postpartum mood and emotional well-being. Now, build upon that conversation by asking a question related to managing stress as a new mother.
Share your thoughts and concerns about stress management and ask for advice on effective techniques to reduce stress and find balance in life.

Example Scenario 1:
User: We previously talked about postpartum mood. I've been struggling with managing stress as a new mother. Can you provide me with some strategies to deal with stress and find balance?

Example Scenario 2:
User: I remember our conversation about postpartum emotional well-being. I'm finding it hard to manage stress in my daily life. Do you have any tips for reducing stress and finding balance as a new mother?
""",
    },
    "linked": {
        "prompt": """
Based on our previous discussions about postpartum care, ask a question related to infant care and feeding. Connect it to the importance of maintaining, well-being while taking care of baby.
Share your thoughts on the challenges of balancing self-care and infant care and ask for tips on how to prioritize self-care without neglecting baby's needs.

Example Scenario 1:
User: We discussed self-care, but I'm finding it challenging to prioritize my well-being while ensuring the best care for my baby. Can you provide some guidance on how to find a balance between self-care and infant care?

Example Scenario 2:
User: Remember when we talked about postpartum care? I'm struggling to take care of myself while caring for my baby. How can I prioritize self-care without neglecting my baby's needs?
""",
    },
    "tree_of_thought": {
        "prompt": """
Imagine a tree representing different aspects of postpartum care. Choose a branch, such as physical recovery or sleep and fatigue, and ask a question related to that aspect. Express concerns or seek advice on specific steps or strategies to promote healing, manage discomfort, or improve sleep quality.

Example Scenario 1:
User: Let's focus on physical recovery after birth. I'm experiencing discomfort and would like to know what steps I can take to promote healing and manage it effectively.

Example Scenario 2:
User: I'm having trouble with sleep and fatigue postpartum. Are there any strategies or techniques you can recommend to improve sleep quality and manage fatigue?
""",
    },
    "instructional": {
        "prompt": """
Provide step-by-step instructions for a self-care practice that promotes relaxation and reduces stress. Describe the practice, its benefits, and guide the user through the process of implementing it in their daily routine.

Example Practice: Deep Breathing Exercise
Step 1: Find a quiet and comfortable place to sit or lie down.
Step 2: Close your eyes and take a deep breath in through your nose, counting to 4.
Step 3: Hold your breath for a moment, then exhale slowly through your mouth, counting to 4.
Step 4: Repeat this breathing pattern for a few minutes, focusing on the sensation of your breath.
Step 5: Notice how your body and mind begin to relax, letting go of tension and stress.

Example Scenario:
User: I'm looking for a self-care practice that can help me relax and reduce stress. Can you provide step-by-step instructions for a practice that I can incorporate into my daily routine?
""",
    },
    "add_examples": {
        "prompt": """
Share an example of a daily routine for self-care practices and helps in managing postpartum anxiety and stress. Describe the activities, their benefits, and how they contribute to overall well-being.

Example Daily Routine:
Morning:
- 15 minutes of meditation for mental clarity and relaxation.
- 30 minutes of light exercise, such as yoga or walking, to boost mood and energy.
- A nutritious breakfast to nourish the body.

Afternoon:
- Engage in a creative activity, like painting or writing, to reduce stress and promote self-expression.
- Take short breaks throughout the day to practice deep breathing exercises and release tension.

Evening:
- Enjoy a warm bath with essential oils for relaxation.
- Read a book or listen to calming music before bed to promote better sleep.

Example Scenario:
User: I need inspiration for a self-care routine. Can you provide an example of a daily routine that balances self-care with the demands of motherhood?
""",
    },
    "style": {
        "prompt": """
Write a persuasive piece on the importance of self-care for new mothers and the positive impact it has on their overall well-being. Use persuasive language and provide compelling arguments to convince the user about the significance of prioritizing self-care.

Example Scenario:
User: I understand the concept of self-care, but can you explain why it's so crucial for new mothers to prioritize their well-being?
""",
    },
    "temperature": {
        "prompt": """
Imagine adjusting the temperature of our conversation to 1, where creativity is at its maximum. Generate a creative response to a question related to postpartum stress and anxiety. Provide a unique and out-of-the-ordinary suggestion to relieve stress.

Example Scenario:
User: I'm looking for a unique and creative way to relieve postpartum stress. Can you suggest something out of the ordinary?
""",
    },
    "open_ended": {
        "prompt": """
        User: How would you describe your experience with infant care and feeding so far?
        User: What are your biggest challenges or concerns when it comes to caring for your newborn?
        User: How do you establish a bond with your infant through feeding and caregiving activities?
        User: How would you describe emotional well-being since becoming a parent?
        User: What are some of the challenges you face in maintaining a positive mood during the postpartum period?
        User: How do you nurture emotional well-being amidst the demands of parenthood?
        User: How has sexuality and sexual desire changed since becoming a parent?
        User: What are the thoughts and feelings about contraception and birth spacing after having a child?
        User: How do you envision balancing sexual needs and the responsibilities of parenthood?
        User: Can you share thoughts on postpartum depression?
        User: Describe the experience with physical recovery after giving birth.How did body feel during the recovery period, and how long did it take for you to start feeling back to normal?
        Context: Postpartum, Anxiety, and Stress
        """
    },
    "instruction": {
        "prompt": """
        User: Reflect on your experiences and write about the most rewarding aspect of infant care for you.
        User: Research different feeding techniques (e.g., breastfeeding, bottle-feeding) and choose one to explore further.
        User: Create a daily care routine for your infant that incorporates feeding, sleep, and playtime.
        User: Reflect on experiences and write about the impact of mood changes on your daily life as a new parent.
        User: Research different strategies for enhancing emotional well-being and choose one to incorporate into routine.
        User: Develop a self-care plan that includes activities to uplift mood and nurture your emotional health.
        User: Reflect on your personal experiences and write about the impact of sexuality on postpartum journey.
        User: Research different contraception methods and their effectiveness, and share your findings.
        User: Develop a plan for birth spacing that aligns with goals and values as a parent.
        User: Provide step-by-step instructions for managing postpartum anxiety.
        User: Provide a step-by-step guide on how to promote physical recovery after giving birth. Include exercises, diet recommendations, and self-care practices to help new mothers regain their strength and energy.
        Context: Postpartum, Anxiety, and Stress
        """
    },
    "multiple_choice": {
        "prompt": """
        ""Which aspect of sexuality do you find most challenging to navigate as a new parent?
        a) Physical intimacy
        b) Emotional connection
        c) Lack of time or energy
         "",

        ""Which contraception method would you prefer to use for birth spacing?
        a) Hormonal methods (e.g., birth control pills, patches)
        b) Barrier methods (e.g., condoms, diaphragms)
        c) Intrauterine devices (IUDs)
        d) Natural methods (e.g., fertility awareness, withdrawal)"",

        ""What are some common symptoms of postpartum anxiety?
        1. Increased heart rate and breathing difficulties
        2. Constant worry and fear
        3. Difficulty sleeping and concentrating
        "",

        ""Which of the following factors can impact the speed and effectiveness of physical recovery after giving birth?
        a) Type of delivery (vaginal or cesarean)
        b) Age of the mother
        c) Prior fitness level
        d) Postpartum complications
        "",

        ""Which emotion do you find most prevalent during the postpartum period?
        a) Happiness
        b) Sadness
        c) Anxiety
        d) Anger
        "",

        ""Which activities help you to improve the mood?
        a) Exercising
        b) Practicing mindfulness or meditation
        c) Engaging in hobbies or creative outlets
        d) Socializing with loved ones"",

        ""Which feeding method have you chosen for your infant?
        a) Breastfeeding
        b) Bottle-feeding with formula
        c) Combination of breastfeeding and formula
        "",

        ""Which aspect of infant care do you find most challenging?
        a) Establishing a feeding routine
        b) Understanding hunger cues
        c) Managing infant sleep patterns
        d) Soothing a fussy baby
        ""

        ""Type here to ask! or to speak and Ask Press 'S' and Enter.
        a) I did not received any input, Please clear the text box and ask again.You can ask by typing in the text box or by Pressing 'S' and Enter to speak and Ask.
        ""
        """
    },
    "fill_in_the_blank": {
        "prompt": """
        User: "Postpartum _______ can have a significant impact on a mother's well-being.",
        "One benefit of practicing effective contraception after childbirth is _______________.",
        "I feel anxious about discussing my sexual needs with my partner because _______________.",
        "To space out my pregnancies, I would consider using _______________ as a contraception method.",
        "The first few weeks after giving birth are often characterized by _________, which can include uterine contractions, breast engorgement, and postpartum bleeding.",
        "Postpartum _______ can have a significant impact on a mother's well-being.",
        "The transition to motherhood can bring about various _______ challenges.",
        "One effective way to manage postpartum stress is through _______ practices.",
        "Postpartum _______ can be improved through proper self-care practices and seeking support from loved ones.",
        "The postpartum period can be improved by addressing anxiety and stress through proper self-care and seeking professional _______.",
        "Hormonal fluctuations during the postpartum phase can be better managed through a _______ approach involving lifestyle changes and support systems.",
        "Engaging in regular physical _______ activities, like gentle exercises or walks, can help improve postpartum anxiety and stress levels.",
        "Postpartum _______ can be alleviated by addressing underlying issues, practicing self-compassion, and seeking professional support.",
        "The postpartum period can be improved by developing a well-rounded support _______ that includes family, friends, and healthcare providers.",
        "Seeking professional _______ is crucial for improving postpartum anxiety and stress and ensuring comprehensive care.",
        "Postpartum _______ can be better managed by prioritizing self-care, setting realistic expectations, and seeking support from loved ones.",
        "The postpartum period can be improved by fostering open communication and _______ strategies with a partner or support network.",
        "Engaging in stress _______ techniques, such as deep breathing or mindfulness exercises, can contribute to improving postpartum anxiety.",
        "Postpartum _______ can be better addressed by seeking professional help, joining support groups, and practicing self-care.",
        "The postpartum period can be improved by focusing on self-________ and making time for activities that promote well-being and relaxation.",
        "Postpartum _______ can be alleviated by engaging in activities that promote relaxation and emotional well-being, such as practicing gratitude or journaling.",
        "The hormonal changes during the postpartum period can be better managed through a holistic _______ that includes healthy lifestyle choices and stress-reduction techniques.",
        "Engaging in social _______ and connecting with other mothers can provide a sense of community and support in improving postpartum anxiety and stress.",
        "Postpartum _______ can be improved by establishing healthy boundaries, prioritizing self-care, and seeking professional guidance when needed.",
        "The postpartum period can be improved by creating a nurturing environment that promotes self-compassion and _______ self-talk.",
        "Postpartum _______ can be better managed by ensuring adequate rest, proper nutrition, and seeking support from healthcare professionals.",
        "The postpartum period can be improved by fostering a positive and supportive _______ that encourages open communication and understanding.",
        "Engaging in relaxation _______ activities, such as yoga or meditation, can contribute to improving postpartum anxiety and stress levels.",
        "Postpartum _______ can be addressed by implementing healthy coping strategies, such as seeking support, engaging in self-care, and practicing stress-management techniques.",
        "One thing I wish I knew before starting infant care is _______________.",
        "I feel most confident in my caregiving abilities when _______________.",
        "My go-to strategy for soothing my baby is _______________.",
        "The postpartum period can be improved by developing a personalized _______ plan that incorporates self-care, professional support, and healthy lifestyle choices."
        Context: Postpartum, Anxiety, and Stress
        """
    },
    "binary": {
        "prompt": """
        User Statements and questions:
        Statements:
        1. Postpartum anxiety can have a significant impact on a mother's well-being.
        2. The transition to motherhood can bring about various challenges related to anxiety and stress.
        3. Many new mothers experience postpartum anxiety as they adjust to their new roles.
        4. Postpartum anxiety can manifest in persistent worry, restlessness, and irritability.
        5. Hormonal changes during the postpartum period can contribute to the development of anxiety symptoms.
        6. Seeking support from healthcare professionals is crucial in managing postpartum anxiety.
        7. Postpartum anxiety can affect the mother-infant bonding and overall parenting experience.
        8. Addressing postpartum anxiety is important for the well-being of both the mother and the baby.
        9. Postpartum anxiety is a common experience that can be effectively treated with appropriate interventions.
        10. Education and awareness about postpartum anxiety are essential to ensure timely support and treatment.
        11. Postpartum anxiety can vary in severity and may require different levels of intervention.
        12. Building a strong support network is beneficial for new mothers experiencing postpartum anxiety.
        13. Self-care practices, such as proper rest and nutrition, can help manage postpartum anxiety.
        14. Postpartum anxiety can be associated with feelings of guilt and self-doubt.
        15. Recognizing the signs and symptoms of postpartum anxiety is important for early intervention.
        16. Engaging in stress-reduction techniques, like deep breathing and mindfulness, can alleviate postpartum anxiety.
        17. Postpartum anxiety may coexist with other mental health conditions, requiring comprehensive evaluation and treatment.
        18. The prevalence of postpartum anxiety underscores the need for accessible mental health services for new mothers.
        19. Partners and family members play a vital role in supporting mothers with postpartum anxiety.
        20. Postpartum anxiety can impact a mother's ability to cope with daily tasks and responsibilities.
        21. Seeking professional help for postpartum anxiety is a sign of strength and proactive self-care.
        22. Postpartum anxiety can affect the overall quality of life and emotional well-being of new mothers.
        23. Postpartum anxiety can interfere with sleep patterns and contribute to sleep disturbances.
        24. Recognizing and validating the experiences of new mothers with postpartum anxiety is essential for reducing stigma.
        25. Postpartum anxiety can be managed through a combination of therapy, medication, and supportive interventions.
        26. Postpartum anxiety may require ongoing monitoring and follow-up care to ensure optimal recovery.
        27. Support groups and peer-to-peer networks can provide valuable emotional support for mothers with postpartum anxiety.
        28. Early identification and intervention for postpartum anxiety can help prevent potential long-term consequences.
        29. Postpartum anxiety can impact the overall mental health and well-being of the entire family unit.
        30. Developing coping mechanisms and stress management strategies can empower mothers with postpartum anxiety.
        31. Postpartum anxiety can be triggered by various factors, including hormonal changes, sleep deprivation, and life stressors.
        32. Encouraging open communication and providing a safe space for mothers to express their feelings is important in addressing postpartum anxiety.
        33. Postpartum anxiety is a valid and treatable condition that should not be dismissed or trivialized.
        34. Engaging in regular physical activity, within the mother's comfort level, can help alleviate postpartum anxiety symptoms.
        35. The impact of postpartum anxiety extends beyond the early postpartum period and may require ongoing support.
        36. Healthcare providers should proactively screen for postpartum anxiety and provide appropriate referrals and resources.
        37. Postpartum anxiety can affect a mother's ability to engage in self-care practices and nurture her own well-being.
        38. Providing education and resources about postpartum anxiety is crucial in promoting early detection and intervention.
        39. Postpartum anxiety can fluctuate in severity throughout the postpartum period and may require different approaches to treatment.
        40. Encouraging mothers to seek support and share their experiences can reduce feelings of isolation and validate their struggles with postpartum anxiety.
        41. Postpartum anxiety can have an impact on a mother's social relationships and may require additional support in maintaining connections.
        42. Nurturing a non-judgmental and supportive environment is essential for mothers with postpartum anxiety to feel comfortable seeking help.
        43. Postpartum anxiety can manifest in physical symptoms, such as headaches, gastrointestinal issues, and muscle tension.
        44. Offering evidence-based psychoeducation to new mothers can help them understand postpartum anxiety and access appropriate treatment options.
        45. Postpartum anxiety can affect a mother's ability to concentrate, make decisions, and manage daily tasks effectively.
        46. Supporting workplace accommodations and flexible schedules for mothers with postpartum anxiety can contribute to their well-being and productivity.
        47. Postpartum anxiety can have long-term consequences if left untreated, emphasizing the importance of early intervention and support.
        48. Is it important to prioritize rest and sleep during the physical recovery period after giving birth.
        questions:
        1. Does postpartum stress impact the overall well-being of new mothers?
        2. Are there effective strategies to manage postpartum stress?
        3. Can postpartum anxiety affect the mother-infant bonding process?
        4. Are there specific risk factors associated with postpartum anxiety?
        5. Do hormonal changes play a role in the development of postpartum anxiety?
        6. Are support groups helpful in addressing postpartum anxiety?
        7. Does postpartum anxiety require professional intervention?
        8. Are there non-medical approaches to managing postpartum anxiety?
        9. Is postpartum anxiety a temporary condition or can it persist for a longer duration?
        10. Can postpartum anxiety impact a mother's ability to care for her newborn?
        11. Are there effective self-care practices for reducing postpartum anxiety?
        12. Does postpartum anxiety require different treatment approaches compared to general anxiety?
        13. Can postpartum anxiety be effectively managed with medication?
        14. Do partners play a significant role in supporting mothers with postpartum anxiety?
        15. Can postpartum anxiety have an impact on a mother's overall mental health?
        16. Are there common signs and symptoms of postpartum anxiety?
        17. Does sleep deprivation contribute to postpartum anxiety?
        18. Can postpartum anxiety affect a mother's social interactions and relationships?
        19. Are there specific coping mechanisms that can alleviate postpartum anxiety?
        20. Does postpartum anxiety increase the risk of developing other mental health disorders?
        21. Can postpartum anxiety affect a mother's decision-making abilities?
        22. Are there long-term consequences associated with untreated postpartum anxiety?
        23. Does postpartum anxiety impact a mother's ability to perform daily tasks?
        24. Can postpartum anxiety affect a mother's physical health?
        25. Are there support resources available specifically for postpartum anxiety?
        26. Does postpartum anxiety affect all new mothers or only a certain percentage?
        27. Can postpartum anxiety be prevented through early intervention?
        28. Are there cultural or societal factors that influence postpartum anxiety?
        29. Does postpartum anxiety affect fathers as well?
        30. Can postpartum anxiety affect the overall well-being of the entire family?
        31. Are there differences between postpartum anxiety and postpartum depression?
        32. Does postpartum anxiety require ongoing monitoring and follow-up care?
        33. Can postpartum anxiety be triggered by specific life stressors?
        34. Are there effective communication strategies for supporting mothers with postpartum anxiety?
        35. Does postpartum anxiety impact a mother's ability to return to work?
        36. Can postpartum anxiety improve with time or does it require treatment?
        37. Are there differences in the prevalence of postpartum anxiety across different cultures?
        38. Does postpartum anxiety affect mothers who have had multiple children differently?
        39. Can postpartum anxiety be present even if a mother did not experience it with a previous child?
        40. Are there effective online resources for mothers with postpartum anxiety?
        41. Does postpartum anxiety affect a mother's self-esteem and self-confidence?
        42. Can postpartum anxiety be managed without medication?
        43. Are there specific relaxation techniques that can help reduce postpartum anxiety?
        44. Does postpartum anxiety affect a mother's ability to enjoy motherhood?
        45. Can postpartum anxiety lead to panic attacks?
        46. Are there gender differences in the experience of postpartum anxiety?
        47. Does postpartum anxiety affect all mothers equally, regardless of their background or circumstances?
        48. Should contraception decisions be a shared responsibility between partners?
        49.Is it important to seek professional guidance or attend parenting classes for infant feeding and care?
        50.Should infant feeding decisions be solely based on the mother's preferences or involve the partner and other caregivers?
        Context: Postpartum, Anxiety, and Stress
        Options:
        1. Yes
        2. No
        """
    },
    "ordering": {
        "prompt": """
        "User: Arrange the strategies for reducing postpartum stress in order of effectiveness, starting from the most effective to the least effective:

        1. Engaging in regular exercise
        2. Practicing deep breathing exercises
        3. Seeking professional therapy or counseling
        4. Creating a support network of family and friends
        5. Implementing stress management techniques, such as meditation or yoga"

        "User: Put the following steps in the correct order for promoting physical recovery after giving birth:

        1.Start with gentle exercises, such as walking or pelvic floor exercises.
        2.Eat a nutritious diet rich in fruits, vegetables, lean proteins, and whole grains.
        3.Practice good hygiene to prevent infection, especially if you had a cesarean delivery.
        4.Get enough rest and sleep whenever possible.
        5.Stay hydrated by drinking plenty of water throughout the day.
        6.Seek guidance from a healthcare professional for postpartum exercises and recovery advice."

        "User: Arrange the stress management techniques for new mothers from most effective to least effective:

        1. Engaging in mindful activities like yoga or meditation
        2. Seeking support from friends and family
        3. Setting realistic expectations and boundaries
        4. Practicing gratitude and positive affirmations
        5. Taking breaks and engaging in hobbies or activities for relaxation
        6. Seeking professional advice from healthcare providers or therapists"

        "User: Prioritize the  self-care activities for reducing postpartum anxiety, with 1 being the highest priority and 3 being the lowest priority:

        1. Taking time for oneself to engage in relaxing activities
        2. Connecting with other new mothers for support and shared experiences
        3. Practicing self-compassion and positive self-talk
        4. Engaging in regular physical exercise to release endorphins and reduce stress"

        "User: Arrange the techniques for managing postpartum stress in order of personal preference, starting with the most preferred:

        1. Engaging in physical activity such as walking or swimming
        2. Participating in relaxation exercises like deep breathing or progressive muscle relaxation
        3. Utilizing stress-relieving techniques such as journaling or creative expression
        4. Practicing mindfulness and meditation to increase present-moment awareness
        5. Setting realistic goals and priorities to reduce overwhelm and pressure"

        "User: Arrange the strategies for managing postpartum anxiety based on preference, starting from the most preferred:

        1. Seeking professional help from a therapist or counselor
        2. Engaging in regular self-care practices
        3. Connecting with support groups or online communities
        4. Educating oneself about postpartum anxiety and its symptoms for better understanding
        5. Incorporating relaxation techniques like deep breathing or progressive muscle relaxation"

        "User: Arrange the following infant care activities in the order of their priority to you:

        (options: feeding, diaper changing, bathing, playtime)"

        "User: Arrange the  methods for improving mental well-being during the postpartum period in order of effectiveness, starting from the most effective:

        1. Engaging in activities that promote relaxation and stress reduction
        2. Establishing a support system of friends and family
        3. Practicing self-care and prioritizing personal needs
        4. Seeking professional guidance for managing mental health concerns"

        "User: Organize the  strategies for managing postpartum stress in order of feasibility, starting with the most feasible:

        1. Incorporating short breaks and self-care moments throughout the day
        2. Seeking support from a postpartum doula or caregiver
        3. Engaging in stress-reducing activities like listening to calming music or nature sounds
        4. Practicing time management and prioritizing tasks effectively
        5. Seeking help from family members or friends with household chores or responsibilities
        6. Setting boundaries and learning to say no to additional commitments or demands"

        "User: Rank the strategies for reducing postpartum stress in order of importance:

        - Engaging in regular exercise
        - Practicing deep breathing exercises
        - Seeking professional therapy or counseling
        - Prioritizing self-care activities
        - Building a strong support network
        - Implementing stress management techniques"

        "User: Rank the  stress management techniques for new mothers based on the effectiveness:

        - Engaging in mindful activities like yoga or meditation
        - Seeking support from friends and family
        - Setting realistic expectations and boundaries
        - Practicing gratitude and positive affirmations
        - Taking breaks and engaging in hobbies or activities for relaxation
        - Seeking professional advice from healthcare providers or therapists"

        "User: Rank the self-care activities for reducing postpartum anxiety in order of the impact:

        - Taking time for oneself to engage in relaxing activities
        - Connecting with other new mothers for support and shared experiences
        - Practicing self-compassion and positive self-talk
        - Engaging in regular physical exercise to release endorphins and reduce stress
        - Seeking therapy or counseling to address underlying anxieties and concerns
        - Creating a calming environment at home, such as with soothing music or aromatherapy"

        "User: Rank the techniques for managing postpartum stress based on personal preference:

        - Engaging in physical activity such as walking or swimming
        - Participating in relaxation exercises like deep breathing or progressive muscle relaxation
        - Utilizing stress-relieving techniques such as journaling or creative expression
        - Practicing mindfulness and meditation to increase present-moment awareness
        - Setting realistic goals and priorities to reduce overwhelm and pressure
        - Seeking social support and sharing feelings with trusted individuals"

        "User: Rank the strategies for managing postpartum anxiety based on preference:

        - Seeking professional help from a therapist or counselor
        - Engaging in regular self-care practices
        - Connecting with support groups or online communities
        - Educating oneself about postpartum anxiety and its symptoms for better understanding
        - Incorporating relaxation techniques like deep breathing or progressive muscle relaxation
        - Developing coping strategies and stress management skills"

        "User: Rank the methods for improving mental well-being during the postpartum period in order of the effectiveness:

        - Engaging in activities that promote relaxation and stress reduction
        - Establishing a support system of friends and family
        - Practicing self-care and prioritizing personal needs
        - Seeking professional guidance for managing mental health concerns
        - Creating a daily routine to provide structure and stability
        - Practicing positive self-talk and nurturing a positive mindset"

        "User: Rank the strategies for managing postpartum stress based on the feasibility:

        - Incorporating short breaks and self-care moments throughout the day
        - Seeking support from a postpartum doula or caregiver
        - Engaging in stress-reducing activities like listening to calming music or nature sounds
        - Practicing time management and prioritizing tasks effectively
        - Seeking help from family members or friends with household chores or responsibilities
        - Setting boundaries and learning to say no to additional commitments or demands"

        "User: Arrange the contraception methods from least effective to most effective:

        (options: condoms, birth control pills, IUDs, fertility awareness)"

        Context: Postpartum, Anxiety, and Stress
        """
    },
    "prediction": {
        "prompt": """
        User: How do you predict your infant's feeding and sleep patterns will evolve as they grow older?
        User: What feeding method do you predict will be the most suitable for your lifestyle and your baby's needs?
        User: How do you think mood and emotional well-being will evolve as your child grows older?
        User: What self-care practice do you predict will have the most significant positive impact on emotional well-being?
        User: How do you think becoming a parent might impact sexual desire in the long term?
        User: What contraception method do you predict would be most suitable for lifestyle and needs?
        User: What are some common physical challenges new mothers may face during the recovery period after giving birth, and how can they be overcome?
        User: What are some potential long-term effects of untreated postpartum anxiety?
        Context: Postpartum, Anxiety, and Stress
        """
    },
    "explanation": {
        "prompt": """
        User: Explain the benefits of breastfeeding for both the infant and the mother.
        User: Describe the signs that indicate your baby is getting enough nourishment during feeding.
        User: Explain the possible factors contributing to mood changes during the postpartum period.
        User: Describe the benefits of engaging in regular physical exercise for emotional well-being
        User: Explain the importance of birth spacing for the health of both the mother and the child.
        User: Describe the effectiveness and potential side effects of different contraception methods.
        User: Explain the role of hormones in the physical recovery process after giving birth. How do hormonal changes affect the body, and what can new mothers expect in terms of physical symptoms and changes?
        User: Can you explain the difference between postpartum anxiety and postpartum depression?
        Context: Postpartum, Anxiety, and Stress
        """
    },
    "opinion": {
        "prompt": """
        User: Share your opinion on the advantages and disadvantages of breastfeeding versus bottle-feeding.
        User: What is your opinion on using pacifiers or comfort objects for soothing a fussy baby?
        User: Share your opinion on the importance of reaching out to friends and family for emotional support during the postpartum period.
        User: What is your opinion on integrating mindfulness or meditation practices into postpartum self-care routines?
        User: Share your opinion on the ideal length of birth spacing between pregnancies and why you believe it is important.
        User: What is your opinion on using natural or non-hormonal contraception methods versus hormonal methods?
        User: In your opinion, what is the most effective exercise or physical activity for aiding in the recovery process after giving birth? Why do you believe it is beneficial?
        User: In your opinion, what is the most effective self-care practice for managing postpartum anxiety?
        Context: Postpartum, Anxiety, and Stress
        """
    },
    "scenario": {
        "prompt": """
        User: Imagine your baby is having difficulty latching during breastfeeding. How would you seek assistance and support?
        User: Suppose you're facing criticism from others for your chosen feeding method. How would you handle this situation and stay confident in your decision?
        User: Imagine you have a friend who is experiencing intense mood swings after giving birth. How would you support and encourage them to seek professional help?
        User: Suppose you're finding it challenging to carve out time for self-care. How would you overcome this obstacle and prioritize emotional well-being?
        User: Imagine you have a close friend who recently became a parent and is struggling with balancing their sexual needs and responsibilities. How would you offer support and guidance to your friend?
        User: Suppose you and your partner have different preferences for contraception methods. How would you handle this situation and come to a mutual decision?
        User: Imagine you are a new mother who had a cesarean delivery. You are experiencing discomfort and limited mobility during the recovery period. Describe the steps you would take to ensure a smooth physical recovery and alleviate any challenges you may face.
        User: Imagine a scenario where a new mother is experiencing severe postpartum anxiety. How would you advise her to seek help and support?
        Context: Postpartum, Anxiety, and Stress
        """
    },
    "comparative": {
        "prompt": """
        User: Compare the benefits of breast milk versus formula for infant nutrition and development.
        User: Compare the advantages and challenges of co-sleeping versus using a separate crib for infant sleep.
        User: Compare the impact of sleep deprivation on mood and emotional well-being in the postpartum period versus other stages of life.
        User: Compare the effectiveness of different relaxation techniques, such as deep breathing exercises, progressive muscle relaxation, and guided imagery.
        User: Compare the advantages and disadvantages of short birth spacing versus longer birth spacing between pregnancies.
        User: Compare the effectiveness and convenience of hormonal contraception methods versus non-hormonal methods.
        User: Compare the physical recovery process after a vaginal birth and a cesarean birth. What are the key differences in terms of healing, pain management, and recommended activities?
        User: Compare the effectiveness of therapy and medication in treating postpartum anxiety.
        Context: Postpartum, Anxiety, and Stress
        """
    }
}
context = "Context: Postpartum, Anxiety, and Stress"

#Recognizing Speech from Voice-Input, i have used Goolge speech recognizer
def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Speak:")
        try:
            audio = recognizer.listen(source, phrase_time_limit=10)# Limiting the recording to 10 seconds
            user_input = recognizer.recognize_google(audio)
            print(f"YOU (Voice): {user_input}")
            return user_input.lower()
        except sr.WaitTimeoutError:
            print("Speech recognition timeout.")
            return ""
        except Exception as e:
            print(f"Speech Recognition error: {e}")
            return ""

# Generating an Answer using OpenAi model Text-da-vinci-003
def generate_answer(question, prompt_technique, context):
    prompt = f'{prompt_technique["prompt"]}Question: {question}\n{context}\nAnswer:'

    # Generate the response from the model
    response = openai.Completion.create(
        engine='text-davinci-003',
        prompt=prompt,
        max_tokens=200,
        temperature=0.1,
        n=1,
        stop=None
    )

    # Extracting the Generated Answer,taking first choice, removing extra spaces
    answer = response.choices[0].text.strip()

    return answer

# Function to speak the response using Pyttsx3
def speak_response(response_text):
    engine = pyttsx3.init()
    engine.say(response_text)
    engine.runAndWait()

def get_user_input():
    user_input = input("YOU!(text): ")

    # If the user enters 'S', proceeding with the voice input
    if user_input.upper() == 'S':
        user_input = recognize_speech()
        return user_input, True
    else:
        return user_input, False

# handling user input and generating chatbot response
def handle_user_input():
    user_input = text_input.get("1.0", tk.END).strip()

    if user_input.lower() == 'exit':
        chat_area.insert(tk.END, "Your Coach, Goodbye!\n")
        return

    # If the user enters 'S', proceed with voice input
    if user_input.upper() == 'S':
        user_input = recognize_speech()

        # Displaying the chatbot's response
        chat_area.insert(tk.END, f"YOU!(Voice): {user_input}\n")
        handle_chatbot_response(user_input, True) 
    else:
        handle_chatbot_response(user_input, False)

def handle_chatbot_response(user_input, voice_input):
    # Searching for the prompt technique 
    prompt_technique = None
    for technique, details in prompt_techniques.items():
        if user_input.lower() in details["prompt"].lower():
            prompt_technique = details
            break

    # Generate the chatbot's response
    if prompt_technique is None:
        # Use the "text-davinci-003" model as a fallback
        answer = generate_answer(user_input, {"prompt": ""},"")
    else:
        answer = generate_answer(user_input, prompt_technique,"")

    # Displaying the chatbot's response
    chat_area.insert(tk.END, f"Coach: {answer}\n")

    # Checking if the input is in voice, then speak the chatbot's response
    if voice_input:
        speak_response(f"YOU : {user_input}")
        speak_response(answer)


def handle_voice_input():
    while True:
        user_input, voice_input = get_user_input()

        # Checking  for the exit command
        if user_input.lower() == 'exit':
            print("Coach: Goodbye!")
            break

        # Speak the chatbot's response for Voice-Input 
        if voice_input:
            handle_chatbot_response(user_input)
            speak_response(answer)

#User Interface-Window
root = tk.Tk()
root.title("Chatbot Interface")
root.configure(bg="white")

#Chatbot Avatar (you can replace 'avatar.png' with the path to your preferred image)
avatar_image = tk.PhotoImage(file='E:/1.png')
avatar_label = tk.Label(root, image=avatar_image)
avatar_label.pack()

#Text label for the  Introduction 
intro_label = tk.Label(root, text="Hello, I am Kingston, your Executive Coach.", font=("Poppins", 15,"bold"), fg="purple")
intro_label.pack()

#Give Input label 
input_label = tk.Label(root, text="Give Input:", font=("Callibri", 12,"bold"), fg="orange")
input_label.pack(side="top", padx=1, pady=1)

#textbox to enter the input text 
text_input = tk.Text(root, height=2, width=80, fg="Black", bg="grey")
text_input.pack()

#to show text inside the text box
text_input.insert("1.0", "Type here to ask! or to speak and Ask Press 'S' and Enter.")


#Output box 
chat_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=100, height=15, fg="white", bg="maroon")
chat_area.pack()

#To show Output will appear here
chat_area.insert("1.0", "Output will appear here...\n")

#Enter box
enter_button = tk.Button(root, text="Enter", command=handle_user_input)
enter_button.pack()

#thread to handle voice, in the background
voice_thread = threading.Thread(target=handle_voice_input)
voice_thread.daemon = True
voice_thread.start()

# S
root.mainloop()