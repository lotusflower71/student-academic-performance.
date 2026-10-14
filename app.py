import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Student Academic Performance", page_icon="🎓", layout="wide")

st.title("🎓 Student Academic Performance Analysis")
st.caption("A simple dashboard to explore marks, grades, and student performance.")

data = {
    "Name": ["Aarav", "Priya", "Rahul", "Ananya", "Rohan", "Sneha"],
    "Maths": [85, 92, 65, 78, 55, 88],
    "Physics": [78, 89, 70, 82, 60, 91],
    "Chemistry": [90, 95, 68, 80, 58, 86],
    "English": [82, 88, 75, 85, 70, 93],
    "Computer": [95, 98, 80, 90, 72, 96],
}
df = pd.DataFrame(data)
subjects = ["Maths", "Physics", "Chemistry", "English", "Computer"]
df["Total"] = df[subjects].sum(axis=1)
df["Percentage"] = df["Total"] / 5

def calculate_grade(p):
    if p >= 90:
        return "A+"
    elif p >= 80:
        return "A"
    elif p >= 70:
        return "B"
    elif p >= 60:
        return "C"
    return "D"

df["Grade"] = df["Percentage"].apply(calculate_grade)
df["Result"] = df[subjects].ge(35).all(axis=1).map({True: "Pass", False: "Fail"})

st.info("This website currently uses sample student data. Replace it with approved data before using it for real students.")

c1, c2, c3, c4 = st.columns(4)
c1.metric("Total students", len(df))
c2.metric("Class average", f'{df["Percentage"].mean():.1f}%')
top = df.loc[df["Percentage"].idxmax()]
low = df.loc[df["Percentage"].idxmin()]
c3.metric("Top performer", top["Name"], f'{top["Percentage"]:.1f}%')
c4.metric("Lowest percentage", f'{low["Percentage"]:.1f}%', low["Name"])

st.subheader("Explore an individual student")
chosen = st.selectbox("Choose a student", df["Name"].tolist())
student = df.loc[df["Name"] == chosen].iloc[0]
a, b, c, d = st.columns(4)
a.metric("Total marks", f'{int(student["Total"])} / 500')
b.metric("Percentage", f'{student["Percentage"]:.1f}%')
c.metric("Grade", student["Grade"])
d.metric("Result", student["Result"])

st.write("**Subject-wise marks**")
marks = pd.DataFrame({"Subject": subjects, "Marks": [int(student[s]) for s in subjects]})
st.bar_chart(marks.set_index("Subject"))

st.subheader("Average marks by subject")
averages = pd.DataFrame({"Subject": subjects, "Average marks": [df[s].mean() for s in subjects]})
st.bar_chart(averages.set_index("Subject"))

st.subheader("Student performance comparison")
comparison = df[["Name", "Percentage"]].sort_values("Percentage", ascending=False).set_index("Name")
st.bar_chart(comparison)

st.subheader("Student ranking")
ranked = df.sort_values("Percentage", ascending=False).reset_index(drop=True)
ranked.index = ranked.index + 1
ranked.index.name = "Rank"
st.dataframe(ranked[["Name", "Total", "Percentage", "Grade", "Result"]].style.format({"Percentage": "{:.1f}%"}), use_container_width=True)

st.subheader("Students below the example 70% support threshold")
support = df[df["Percentage"] < 70][["Name", "Percentage", "Grade"]]
if support.empty:
    st.success("No students are below 70% in this sample.")
else:
    st.dataframe(support.style.format({"Percentage": "{:.1f}%"}), use_container_width=True)
st.caption("Grades and the 70% support threshold are illustrative project rules, not official college policies.")
