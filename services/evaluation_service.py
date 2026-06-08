from services.rag_service import (
    recruiter_chat
)


def evaluate_rag(
    question,
    expected_answer,
    db
):

    result = recruiter_chat(
        question,
        db
    )

    actual_answer = result["answer"]

    passed = (
        expected_answer.lower()
        in actual_answer.lower()
    )

    return {
        "question": question,
        "expected_answer": expected_answer,
        "actual_answer": actual_answer,
        "passed": passed
    }

def evaluate_rag_batch(
    evaluations,
    db
):

    results = []

    passed_count = 0

    for item in evaluations:

        result = evaluate_rag(
            item.question,
            item.expected_answer,
            db
        )

        if result["passed"]:

            passed_count += 1

        results.append(
            result
        )

    total = len(results)

    accuracy = 0

    if total > 0:

        accuracy = round(
            (passed_count / total) * 100,
            2
        )

    return {

        "total_tests": total,

        "passed": passed_count,

        "failed": total - passed_count,

        "accuracy": accuracy,

        "results": results
    }
