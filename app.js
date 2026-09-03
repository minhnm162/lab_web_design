const form = document.getElementById("score-form");

if (form) {
    form.addEventListener("submit", function(event) {
        event.preventDefault();

        const subjects = ["mon1", "mon2", "mon3"].map(function(id, index) {
            return {
                name: "Subject " + (index + 1),
                score: Number(document.getElementById(id).value)
            };
        });

        const total = subjects.reduce(function(sum, subject) {
            return sum + subject.score;
        }, 0);
        const average = total / subjects.length;
        const above8 = subjects.filter(function(subject) {
            return subject.score > 8;
        });
        const highest = subjects.reduce(function(best, subject) {
            return subject.score > best.score ? subject : best;
        });

        document.getElementById("total").textContent = total.toFixed(2);
        document.getElementById("average").textContent = average.toFixed(2);
        document.getElementById("highest").textContent = highest.score.toFixed(2);
        document.getElementById("highest-subject").textContent = highest.name;
        document.getElementById("above8").textContent = above8.length
            ? "Subjects above 8: " + above8.map(function(subject) { return subject.name; }).join(", ")
            : "No subject scored above 8.";

        const status = average >= 8 ? "Excellent result" : average >= 5 ? "Passed" : "Needs improvement";
        document.getElementById("grade-status").textContent = status;
        document.getElementById("message").textContent = average >= 5
            ? "Bạn đã hoàn thành bài thi với kết quả đạt."
            : "Hãy xem lại các môn có điểm thấp để cải thiện kết quả.";
    });
}
