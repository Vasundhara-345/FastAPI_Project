import matplotlib.pyplot as plt
import pandas as pd

from data_patient import data_dict

# Create a Pandas DataFrame from the data dictionary
df = pd.DataFrame(data_dict)

# Plot 1: Admitted vs Rehabilitated Patients
admitted_count = len([entry for entry in data_dict if entry['rehabilitation_status'] == 'Admitted'])
rehabilitated_count = len([entry for entry in data_dict if entry['rehabilitation_status'] in ['Completed', 'Left Against Medical Advice', 'Transferred']])

labels = ['Admitted', 'Rehabilitated']
values = [admitted_count, rehabilitated_count]

plt.bar(labels, values, color=["blue","green"])
plt.xlabel('Status')
plt.ylabel('Count')
plt.title('Admitted vs Rehabilitated Patients')
plt.show()

# Plot 2: Age Groups
age_groups = [entry['age'] for entry in data_dict]
age_bins = [18, 25, 35, 45, 55, 65]
age_labels = ['18-24', '25-34', '35-44', '45-54', '55-64']

age_counts = [len([age for age in age_groups if age_bin[0] <= age < age_bin[1]]) for age_bin in zip(age_bins, age_bins[1:])]

plt.bar(age_labels, age_counts, color=['red','green','grey','black'])
plt.xlabel('Age Group')
plt.ylabel('Count')
plt.title('Age Groups')
plt.show()

# Plot 3: Most Common Drugs
drugs = [entry['type_of_drug'] for entry in data_dict]
drug_counts = pd.Series(drugs).value_counts()

plt.bar(drug_counts.index, drug_counts.values, color=['red','blue','green','grey','black','orange'])
plt.xlabel('Drug')
plt.ylabel('Count')
plt.title('Most Common Drugs')
plt.show()