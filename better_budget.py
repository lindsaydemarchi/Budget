import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

def reading():
	temp = pd.read_csv('credit.csv', header=3)
	df = temp.loc[(temp["Category"] == 'DEBIT')]

	total = np.sum(df["Amount"])
	print('You have spent ${:.2f} this month.' . format(abs(total)))

	return df, abs(total)

def get_categories(dataframe, keywords):
	sub_dfs = {}
	for key in keywords:
		bool_mask = [any([k in d.lower() for k in keywords[key]]) for d in dataframe['Description'].tolist()]
		sub_dfs[key] = dataframe.loc[bool_mask]
	return sub_dfs


def amounts_by_keyword(dataframe, keywords):
        kw_amounts = {k: abs(dataframe.loc[[k in d.lower() for d in dataframe['Description'].tolist()]]['Amount'].sum()) for k in keywords}
        return kw_amounts

def compare_budget(dataframes, budget, total):
	total_spent = 0
	for key in budget:
		spent = np.abs(sub_dfs[key]['Amount'].sum())
		saved = budget[key] - spent
		total_spent += abs(spent)
		if saved > 0:
			print('Of your {} budget, you have spent ${:.2f}, and saved ${:.2f}.' . format(key, spent, saved))
		else: 
			print('Oops! In your {} budget, you have spent ${:.2f}, which is ${:.2f} over budget.' . format(key, spent, abs(saved)))
	print('there is {} unaccounted for.' . format(total - total_spent))

def plot_budget(dataframes, budget_dict, keyword_dict):
	cat_totals = {k: abs(v['Amount'].sum()) for k, v in dataframes.items()}
	cat_labels = [str(k) for k in dataframes]

	fig, ax = plt.subplots()
        # plot budgeted amounts
	plt.bar(cat_labels, [budget_dict[l] for l in cat_labels], alpha=0.6)
        # plot spent amounts, broken down first by category then by keyword
        colors = ['C{}'.format(i) for i in range(1, 10)]
        for cat in keyword_dict:
            kw_amounts = amounts_by_keyword(dataframes[cat], keyword_dict[cat])
            sorted_keys = sorted(kw_amounts, key=lambda x: kw_amounts[x], reverse=True)
            for i, k in enumerate(sorted_keys):
                bottom = sum(sorted(kw_amounts.values(), reverse=True)[:i])
                plt.bar(cat, kw_amounts[k], bottom=bottom, color=colors[i], alpha=0.6)
	plt.show()

keywords = {
	'fun': ['soc', 'puff', 'diner', 'beer'],
	'food': ['tech', 'fresh'],
	'coffee': ['coffee', 'cafe', 'intelligentsia'],
	'travel': ['american'],
	'utilities': [],
	'rent': [],
	'misc':['spotify']
}

budget = {
	'fun': 200.,
	'food': 240.,
	'coffee': 50.,
	'travel':200.,
	'utilities': 150.,
	'rent': 900.,
	'misc': 50.
}

df, total = reading()
sub_dfs = get_categories(df, keywords)
compare_budget(sub_dfs, budget, total)

plot_budget(sub_dfs, budget, keywords)

