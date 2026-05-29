from analyzer import AnalysisResult


GRADE_THRESHOLDS = [
    (9.0, "A", "Excellent"),
    (7.5, "B", "Good"),
    (6.0, "C", "Fair"),
    (4.0, "D", "Needs Work"),
    (0.0, "F", "Poor"),
]

BADGE_COLORS = {
    "Excellent": "#2ecc71",
    "Good": "#3498db",
    "Fair": "#f39c12",
    "Needs Work": "#e67e22",
    "Poor": "#e74c3c",
}


class CommunicationScorer:
    def __init__(self, weights: dict, max_score: float = 10.0):
        self.filler_weight = weights.get("filler_penalty", 0.4)
        self.grammar_weight = weights.get("grammar_penalty", 0.3)
        self.clarity_weight = weights.get("clarity_bonus", 0.3)
        self.max_score = max_score

    def compute_score(self, result: AnalysisResult, word_count: int) -> float:
        filler_rate = result.filler_word_count / max(word_count, 1)
        filler_score = max(0.0, 10.0 - (filler_rate * 100))

        grammar_score = max(0.0, 10.0 - (len(result.grammar_errors) * 1.5))

        final = (
            filler_score * self.filler_weight
            + grammar_score * self.grammar_weight
            + result.clarity_score * self.clarity_weight
        )
        return round(min(final, self.max_score), 1)

    def get_grade(self, score: float) -> tuple[str, str, str]:
        for threshold, grade, badge in GRADE_THRESHOLDS:
            if score >= threshold:
                return grade, badge, BADGE_COLORS[badge]
        return "F", "Poor", BADGE_COLORS["Poor"]
