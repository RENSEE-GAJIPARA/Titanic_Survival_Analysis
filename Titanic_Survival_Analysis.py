#Titanic Survival Analysis — EDA with Dashboard

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import seaborn as sns

sns.set_theme(style="whitegrid", palette="muted")
plt.rcParams.update({"figure.dpi": 130, "font.family": "DejaVu Sans"})

COLORS = {"survived": "#2ecc71", "died": "#e74c3c", "accent": "#3498db", "male": "#3498db", "female": "#9b59b6"}


#LOADING & OVERVIEW
print("=" * 55)
print("TITANIC SURVIVAL ANALYSIS — EDA WITH DASHBOARD")
print("=" * 55)

df = pd.read_csv("Titanic-Dataset.csv")

print("\nDataset Loaded!!")
print(f"Rows : {df.shape[0]}")
print(f"Columns : {df.shape[1]}")
print(f"\nFirst 5 Rows : \n{df.head()}")
print(f"\nData Types : \n{df.dtypes}")
print(f"\nBasic Statistics : \n{df.describe().round(2)}")


#DATA CLEANING
print(f"\n{"=" * 55}")
print("DATA CLEANING")
print("=" * 55)

missing = df.isnull().sum()
missing_pct = (missing / len(df) * 100).round(2)
mv = pd.DataFrame({"Missing Count": missing, "Missing %": missing_pct})
print(f"\nMissing Values (Before):\n{mv[mv['Missing Count']>0].to_string()}")

df["Age"].fillna(df["Age"].median(), inplace=True)
print(f"\nNull Ages are filled with median Age.")

df["Embarked"].fillna(df["Embarked"].mode()[0], inplace=True)
print(f"\nNull Embarked are filled with Mode.")

df.drop(columns="Cabin", inplace=True)
print("\nCabin Dropped!!")

df["AgeGroup"] = pd.cut(df["Age"], bins=[0, 12, 18, 35, 60, 100], 
                        labels=["Child", "Teen", "Young Adult", "Adult", "Senior"])
print("\nAgeGroup feature created.")
print(f"\nMissing after cleaning : {df.isna().sum().sum()}")


#INSIGHTS & SUMMARY
print(f"\n{"=" * 55}")
print("INSIGHTS & SUMMARY")
print("=" * 55)

print(f"\nOverall Survival Rate : {df['Survived'].mean()*100:.1f}%")
print(f"\nSurvival by Gender : \n{df.groupby("Sex")["Survived"].mean().mul(100).round(1)}")
print(f"\nSurvival by Class : \n{df.groupby("Pclass")["Survived"].mean().mul(100).round(1)}")
print(f"\nSurvival by Age Group : \n{df.groupby("AgeGroup")["Survived"].mean().mul(100).round(1)}")


#DASHBOARD
fig = plt.figure(figsize=(18, 12))


# Title Banner
fig.text(0.5, 0.9, "TITANIC SURVIVAL ANALYSIS DASHBOARD", ha="center", va="top", fontsize=20, fontweight="bold", color="#2c3e50")
fig.text(0.5, 0.94, "Exploratory Data Analysis  |  891 Passengers  |  Kaggle Dataset", ha="center", va="top", fontsize=11, color="#7f8c8d")
gs = gridspec.GridSpec(2, 3, figure=fig, hspace=0.45, wspace=0.35, left=0.06, right=0.97, top=0.91, bottom=0.06)


#Pie Chart
ax1 = fig.add_subplot(gs[0, 0])
counts = df["Survived"].value_counts().sort_index()
ax1.pie(counts, labels=["Did Not Survive", "Survived"], autopct="%1.1f%%", startangle=140, explode=(0.04, 0.04),
        colors=[COLORS["died"], COLORS["survived"]], wedgeprops={"edgecolor": "white", "linewidth": 2}, textprops={"fontsize": 10})
ax1.set_title("Overall Survival", fontsize=12, fontweight="bold", pad=10)


#Survival by Gender (Bar Chart)
ax2 = fig.add_subplot(gs[0, 1])
gender_surv = df.groupby("Sex")["Survived"].mean().mul(100).reset_index()
gender_surv.columns = ["Sex", "SurvivalRate"]
pal = [COLORS["female"] if s == "female" else COLORS["male"] for s in gender_surv["Sex"]]
bars = ax2.bar(gender_surv["Sex"], gender_surv["SurvivalRate"], color=pal, edgecolor="white", width=0.4)

for bar, val in zip(bars, gender_surv["SurvivalRate"]):
    ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.8, f"{val:.1f}%", ha="center", va="bottom", fontweight="bold", fontsize=10)

ax2.set_title("Survival Rate by Gender", fontsize=12, fontweight="bold")
ax2.set_ylabel("Survival Rate (%)")
ax2.set_ylim(0, 100)


# Class + Gender grouped (Bar Chart)
ax3 = fig.add_subplot(gs[0, 2])
class_gender = df.groupby(["Pclass", "Sex"])["Survived"].mean().mul(100).unstack()
class_gender.index = ["Class 1", "Class 2", "Class 3"]
class_gender.plot(kind="bar", ax=ax3, color=[COLORS["female"], COLORS["male"]], edgecolor="white", width=0.6, rot=0)

for bar in ax3.patches:
    ax3.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.8,
            f"{bar.get_height():.0f}%", ha="center", va="bottom", fontsize=8, fontweight="bold")

ax3.set_title("Survival by Class & Gender", fontsize=12, fontweight="bold")
ax3.set_ylabel("Survival Rate (%)")
ax3.set_ylim(0, 115)
ax3.legend(title="Gender", fontsize=9)


#Age Group (Bar Chart)
ax4 = fig.add_subplot(gs[1, 0])
age_surv = df.groupby("AgeGroup", observed=True)["Survived"].mean().mul(100).reset_index()
age_surv.columns = ["AgeGroup", "SurvivalRate"]
bars = ax4.bar(age_surv["AgeGroup"], age_surv["SurvivalRate"], color=COLORS["accent"], edgecolor="white", width=0.5)

for bar, val in zip(bars, age_surv["SurvivalRate"]):
    ax4.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
            f"{val:.1f}%", ha="center", va="bottom", fontweight="bold", fontsize=9)

ax4.set_title("Survival Rate by Age Group", fontsize=12, fontweight="bold")
ax4.set_xlabel("Age Group")
ax4.set_ylabel("Survival Rate (%)")
ax4.set_ylim(0, 80)
ax4.tick_params(axis='x', labelsize=9)


#Heatmap
ax5 = fig.add_subplot(gs[1, 1:])
hmap = df.pivot_table(values="Survived", index="Pclass", columns="Sex", aggfunc="mean").mul(100).round(1)
hmap.index = [f"Class {i}" for i in hmap.index]
sns.heatmap(hmap, annot=True, fmt=".1f", cmap="RdYlGn",
            linewidths=0.5, linecolor="white", ax=ax5,
            cbar_kws={"label": "Survival Rate (%)"},
            annot_kws={"size": 16, "weight": "bold"})
ax5.set_title("Survival Rate (%) — Class × Gender Heatmap", fontsize=12, fontweight="bold")
ax5.set_xlabel("Gender")
ax5.set_ylabel("Passenger Class")

plt.savefig("Titanic_Dashboard.png", bbox_inches="tight", dpi=150, facecolor=fig.get_facecolor())
plt.close()
print("\nSaved: titanic_dashboard.png")
print(f"\n{"=" * 55}")
print("  ALL DONE!")
print("=" * 55)