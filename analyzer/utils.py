"""NLP-style message analysis utilities."""

import re
from typing import Dict, List, Tuple


# Weighted keyword dictionaries
AFFECTION_WORDS = {
    # High closeness (5)
    'love': 5, 'adore': 5, 'miss you': 5, 'miss': 4, 'love you': 5,
    'baby': 4, 'honey': 4, 'sweetie': 4, 'dear': 4, 'darling': 5,
    'heart': 4, 'soulmate': 5, 'forever': 4, 'always': 3, 'bestie': 5,
    'best friend': 5, 'bestie': 5, 'soulmate': 5, 'partner': 4,
    # Medium-high closeness (4)
    'care': 3, 'care about': 4, 'missed': 3, 'loving': 4, 'cherish': 4,
    'means a lot': 4, 'appreciate': 3, 'grateful': 3, 'thankful': 3,
    # Emotional expressions
    'hug': 3, 'hugs': 4, 'kiss': 4, 'kisses': 4, 'hold': 3,
}

NEGATIVE_EMOTION_WORDS = {
    # Negative emotions (can indicate close relationship despite negativity)
    'hate': 2, 'angry': 2, 'mad': 2, 'upset': 2, 'frustrated': 2,
    'annoyed': 2, 'hurt': 3, 'sad': 2, 'cry': 3, 'crying': 3,
    'tears': 3, 'sorry': 3, 'apologize': 3, 'forgive': 4,
}

FORMAL_WORDS = {
    # Very formal (indicates teacher/coworker/stranger)
    'dear': 5, 'regards': 5, 'sincerely': 5, 'respectfully': 5,
    'yours truly': 5, 'yours faithfully': 5, 'kind regards': 5,
    'best regards': 5, 'to whom it may concern': 5,
    # Formal
    'please': 3, 'thank you': 3, 'thanks': 2, 'appreciate': 3,
    'regarding': 4, 'concerning': 4, 'according to': 4,
    'informed': 4, 'request': 3, 'require': 4, 'assistance': 4,
    'consult': 4, 'discuss': 3, 'schedule': 3, 'appointment': 3,
    'meeting': 3, 'conference': 4, 'proposal': 4, 'report': 4,
    'document': 4, 'policy': 4, 'procedure': 4, 'guidelines': 4,
    # Academic/work
    'professor': 5, 'doctor': 5, 'sir': 4, 'madam': 4,
    'supervisor': 4, 'manager': 4, 'director': 4, 'colleague': 4,
    'faculty': 5, 'academic': 5, 'research': 4,
}

SLANG_WORDS = {
    # Friend/close indicators
    'bro': 4, 'bruh': 4, 'dude': 3, 'man': 2, 'hey': 1,
    'lol': 3, 'lmao': 4, 'rofl': 4, 'haha': 2, 'hahaha': 3,
    'omg': 4, 'omfg': 4, 'wtf': 3, 'wth': 3, 'bruh': 4,
    'gonna': 2, 'wanna': 2, 'gotta': 2, 'kinda': 2, 'sorta': 2,
    'yeah': 1, 'yep': 1, 'nope': 1, 'nah': 1,
    'cool': 2, 'nice': 1, 'awesome': 3, 'lit': 4, 'fire': 4,
    'sus': 3, 'cap': 3, 'no cap': 4, 'bet': 3, 'highkey': 4,
    'lowkey': 3, 'vibe': 3, 'vibes': 3, 'mood': 3,
}

EMOJI_PATTERNS = {
    # Emotional emojis
    '❤️': 5, '💕': 5, '💖': 5, '💗': 5, '💓': 5, '💞': 5, '💕': 5,
    '😍': 5, '🥰': 5, '😘': 4, '😻': 4,
    '😭': 4, '😢': 3, '💔': 4, '😿': 3,
    '😀': 2, '😄': 2, '😁': 2, '😂': 3, '🤣': 4,
    '👍': 2, '👎': 2, '👋': 2, '🙏': 3,
    '💯': 4, '🔥': 4, '✨': 3, '⭐': 2,
}


def count_word_matches(text: str, word_dict: Dict[str, int]) -> Tuple[int, List[str]]:
    """Count matches and return total score + matched words."""
    text_lower = text.lower()
    total_score = 0
    matched_words = []
    
    # Sort by length descending to match longer phrases first
    sorted_words = sorted(word_dict.keys(), key=len, reverse=True)
    
    for word in sorted_words:
        if word in text_lower:
            total_score += word_dict[word]
            matched_words.append(word)
    
    return total_score, matched_words


def count_emojis(text: str) -> Tuple[int, List[str]]:
    """Count emoji matches."""
    total_score = 0
    matched_emojis = []
    
    for emoji, score in EMOJI_PATTERNS.items():
        count = text.count(emoji)
        if count > 0:
            total_score += score * count
            matched_emojis.extend([emoji] * count)
    
    return total_score, matched_emojis


def analyze_formality(text: str) -> Dict:
    """Analyze the formality level of the message."""
    score, matches = count_word_matches(text, FORMAL_WORDS)
    
    # Normalize by text length
    word_count = len(text.split())
    if word_count > 0:
        normalized_score = min(10, (score / word_count) * 10)
    else:
        normalized_score = 0
    
    # Determine formality level
    if normalized_score >= 3:
        level = 'very_formal'
    elif normalized_score >= 1.5:
        level = 'formal'
    elif normalized_score >= 0.5:
        level = 'neutral'
    else:
        level = 'informal'
    
    return {
        'score': round(normalized_score, 2),
        'level': level,
        'matched_words': matches[:5],  # Limit to top 5
    }


def analyze_emotional_tone(text: str) -> Dict:
    """Analyze the emotional intensity of the message."""
    affection_score, affection_matches = count_word_matches(text, AFFECTION_WORDS)
    negative_score, negative_matches = count_word_matches(text, NEGATIVE_EMOTION_WORDS)
    emoji_score, emoji_matches = count_emojis(text)
    
    total_emotion = affection_score + negative_score + emoji_score
    
    # Normalize
    word_count = len(text.split())
    if word_count > 0:
        normalized_score = min(10, (total_emotion / word_count) * 10)
    else:
        normalized_score = 0
    
    # Determine emotional level
    if normalized_score >= 3:
        level = 'very_emotional'
    elif normalized_score >= 1.5:
        level = 'emotional'
    elif normalized_score >= 0.5:
        level = 'neutral'
    else:
        level = 'flat'
    
    all_matches = affection_matches + negative_matches + emoji_matches
    
    return {
        'score': round(normalized_score, 2),
        'level': level,
        'matched_words': all_matches[:5],
        'affection_score': affection_score,
        'negative_score': negative_score,
        'emoji_score': emoji_score,
    }


def analyze_slang(text: str) -> Dict:
    """Analyze slang usage in the message."""
    score, matches = count_word_matches(text, SLANG_WORDS)
    
    # Normalize
    word_count = len(text.split())
    if word_count > 0:
        normalized_score = min(10, (score / word_count) * 10)
    else:
        normalized_score = 0
    
    # Determine slang level
    if normalized_score >= 2:
        level = 'very_casual'
    elif normalized_score >= 1:
        level = 'casual'
    elif normalized_score >= 0.3:
        level = 'slightly_casual'
    else:
        level = 'standard'
    
    return {
        'score': round(normalized_score, 2),
        'level': level,
        'matched_words': matches[:5],
    }


def calculate_closeness(formality: Dict, emotional: Dict, slang: Dict) -> Tuple[int, str]:
    """Calculate the closeness level (1-5)."""
    closeness = 5  # Start high, deduct for formal
    
    # Deduct for formality
    if formality['level'] == 'very_formal':
        closeness -= 4
    elif formality['level'] == 'formal':
        closeness -= 3
    elif formality['level'] == 'neutral':
        closeness -= 1
    
    # Add for emotional
    if emotional['level'] == 'very_emotional':
        closeness += 2
    elif emotional['level'] == 'emotional':
        closeness += 1
    
    # Add for slang (casual = closer relationship)
    if slang['level'] in ['very_casual', 'casual']:
        closeness += 1
    elif slang['level'] == 'slightly_casual':
        closeness += 0
    
    # Clamp to 1-5
    closeness = max(1, min(5, closeness))
    
    # Map to description
    closeness_labels = {
        1: 'distant',
        2: 'somewhat distant',
        3: 'acquaintance',
        4: 'close',
        5: 'very close',
    }
    
    return closeness, closeness_labels[closeness]


def determine_recipient_type(formality: Dict, emotional: Dict, slang: Dict, closeness: int) -> Tuple[str, int]:
    """Determine the likely recipient type and confidence."""
    
    # Scoring for each recipient type
    scores = {
        'friend': 0,
        'parent': 0,
        'teacher': 0,
        'crush': 0,
        'stranger': 0,
        'coworker': 0,
    }
    
    # Formal indicators -> teacher/coworker/stranger
    if formality['level'] in ['very_formal', 'formal']:
        scores['teacher'] += 5
        scores['coworker'] += 4
        scores['stranger'] += 3
        scores['parent'] -= 2
        scores['friend'] -= 3
        scores['crush'] -= 2
    
    # Informal + emotional -> crush/close friend/parent
    if emotional['level'] in ['very_emotional', 'emotional']:
        scores['crush'] += 4
        scores['parent'] += 4
        scores['friend'] += 3
    
    # High closeness + affection -> crush/parent
    if closeness >= 4:
        if emotional.get('affection_score', 0) > emotional.get('negative_score', 0):
            scores['crush'] += 3
            scores['parent'] += 2
    
    # Casual slang -> friend
    if slang['level'] in ['very_casual', 'casual']:
        scores['friend'] += 4
        scores['crush'] += 2
        scores['parent'] += 1
        scores['teacher'] -= 3
        scores['coworker'] -= 2
    
    # Specific patterns
    if 'mom' in emotional.get('matched_words', []) or 'dad' in emotional.get('matched_words', []):
        scores['parent'] += 5
    
    # Find highest score
    max_score = max(scores.values())
    if max_score <= 0:
        recipient = 'stranger'
        confidence = 30
    else:
        recipient = max(scores, key=scores.get)
        # Calculate confidence based on gap between top 2 scores
        sorted_scores = sorted(scores.values(), reverse=True)
        if len(sorted_scores) >= 2:
            gap = sorted_scores[0] - sorted_scores[1]
            confidence = min(95, 50 + gap * 10)
        else:
            confidence = 60
    
    return recipient, confidence


def generate_explanation(formality: Dict, emotional: Dict, slang: Dict, 
                         recipient: str, closeness: int) -> str:
    """Generate a human-readable explanation of the analysis."""
    parts = []
    
    # Formality observation
    if formality['level'] == 'very_formal':
        parts.append("uses very formal language")
    elif formality['level'] == 'formal':
        parts.append("uses formal language")
    elif formality['level'] == 'informal':
        parts.append("uses casual language")
    
    # Emotional observation
    if emotional['level'] in ['very_emotional', 'emotional']:
        if emotional.get('affection_score', 0) > emotional.get('negative_score', 0):
            parts.append("expresses positive emotions like affection")
        else:
            parts.append("expresses strong (possibly negative) emotions")
    elif emotional['level'] == 'flat':
        parts.append("has a neutral emotional tone")
    
    # Slang observation
    if slang['level'] in ['very_casual', 'casual']:
        parts.append("contains slang and informal expressions")
    
    # Build explanation
    if not parts:
        explanation = "This message has a neutral tone with no strong indicators."
    else:
        explanation = "This message " + ", ".join(parts) + "."
    
    # Add recipient hint
    recipient_hints = {
        'friend': " It appears to be intended for a friend.",
        'parent': " It seems directed at a family member.",
        'teacher': " It appears formal enough for a teacher or professor.",
        'crush': " The emotional tone suggests a romantic interest.",
        'stranger': " The formal nature suggests a stranger or professional contact.",
        'coworker': " It seems appropriate for a coworker or professional contact.",
    }
    
    explanation += recipient_hints.get(recipient, "")
    
    return explanation


def analyze_message(message: str) -> Dict:
    """
    Main function to analyze a message and predict recipient type and closeness.
    
    Returns:
        Dictionary containing:
        - recipient_type: The predicted recipient (friend, parent, teacher, crush, stranger, coworker)
        - closeness: Level 1-5 (distant to very close)
        - closeness_label: Text description of closeness
        - confidence: Confidence score 0-100%
        - explanation: Human-readable explanation
        - breakdown: Detailed scores
    """
    # Run all analyses
    formality = analyze_formality(message)
    emotional = analyze_emotional_tone(message)
    slang = analyze_slang(message)
    
    # Calculate closeness
    closeness, closeness_label = calculate_closeness(formality, emotional, slang)
    
    # Determine recipient
    recipient, confidence = determine_recipient_type(formality, emotional, slang, closeness)
    
    # Generate explanation
    explanation = generate_explanation(formality, emotional, slang, recipient, closeness)
    
    # Build result
    result = {
        'recipient_type': recipient,
        'closeness': closeness,
        'closeness_label': closeness_label,
        'confidence': confidence,
        'explanation': explanation,
        'breakdown': {
            'formality_score': formality['score'],
            'formality_level': formality['level'],
            'emotional_score': emotional['score'],
            'emotional_level': emotional['level'],
            'slang_score': slang['score'],
            'slang_level': slang['level'],
        },
    }
    
    return result