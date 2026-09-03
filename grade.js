// Array chứa các Object
const subjects = [
    {
        name: "Math",
        score: 9
    },

    {
        name: "English",
        score: 7.5
    },

    {
        name: "Physics",
        score: 8.5
    }
];


// =========================
// 1. IN DANH SÁCH MÔN HỌC
// =========================

const subjectList = document.getElementById("subject-list");

if (subjectList) {
    for (let i = 0; i < subjects.length; i++) {

        const li = document.createElement("li");

        li.textContent =
            subjects[i].name +
            ": " +
            subjects[i].score;

        subjectList.appendChild(li);
    }
}


// =========================
// 2. TÍNH TỔNG
// =========================

let total = 0;

for (let i = 0; i < subjects.length; i++) {

    total = total + subjects[i].score;

}

console.log("Total:", total);

document.getElementById("total").textContent =
    "Total score: " + total;


// =========================
// 3. TÍNH TRUNG BÌNH
// =========================

let average = total / subjects.length;

console.log("Average:", average);

document.getElementById("average").textContent =
    "Average score: " + average.toFixed(2);


// =========================
// 4. CÁC MÔN ĐIỂM > 8
// =========================

const above8List =
    document.getElementById("above8");

for (let i = 0; i < subjects.length; i++) {

    if (subjects[i].score > 8) {

        console.log(
            subjects[i].name,
            subjects[i].score
        );

        const li =
            document.createElement("li");

        li.textContent =
            subjects[i].name +
            ": " +
            subjects[i].score;

        above8List.appendChild(li);
    }
}


// =========================
// 5. TÌM HIGHEST SCORE
// =========================

let highest = subjects[0];

for (let i = 1; i < subjects.length; i++) {

    if (subjects[i].score > highest.score) {

        highest = subjects[i];

    }

}

console.log(
    "Highest score:",
    highest.name,
    highest.score
);

document.getElementById("highest").textContent =
    highest.name +
    ": " +
    highest.score;