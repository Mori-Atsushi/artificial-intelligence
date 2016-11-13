# -*- coding:utf-8 -*-
#単連結法 凝集型クラスタリング

import MeCab

NUM =  100	#記事数
GROUP = 3	#分類数

class Article:
	"""記事クラス"""

	def __init__(self, fileName):
		self.words = {}
		mt = MeCab.Tagger('-Ochasen')
		for line in open(fileName, 'r'):
			mecabLine = mt.parse(line)
			mecabWords = mecabLine.split('\n')
			for mecabWord in mecabWords:
				if not(mecabWord == 'EOS' or mecabWord == ''):
					mecabElems = mecabWord.split('\t')
					if mecabElems[2] in self.words:
						self.words[mecabElems[2]] += 1
					else:
						self.words[mecabElems[2]] = 1
		self.words = sorted(self.words.items())

	def calcSimilar(self, comparison):
		similar = 0
		last = 0
		for i in range(0, len(self.words)):
			for j in range(last, len(comparison.words)):
				if self.words[i][0] < comparison.words[j][0]:
					last = j
					break
				elif self.words[i][0] == comparison.words[j][0]:
					similar += self.words[i][1] * comparison.words[j][1]
		return similar

if __name__ == '__main__':
	article = {}
	similar = {}
	group = []
	history = []

	#前処理（mecab処理、類似度計算）
	for i in range(0, NUM):
		group.append([])
		group[i].append(i)
		article[i] = Article('./data/%02d.txt'%i)
		similar[i] = {}
		for j in range(0, i):
			similar[i][j] = article[i].calcSimilar(article[j])

	#クラスタリング
	while len(group) > GROUP:
		mini = 1
		minj = 0
		minsample1 = group[mini][0]
		minsample2 = group[minj][0]

		for i in range(0, len(group)):
			for j in range(0, i):
				maxsample1 = group[i][0]
				maxsample2 = group[j][0]
				for sample1 in group[i]:
					for sample2 in group[j]:
						if sample1 < sample2:
							s1, s2 = sample2, sample1
						else:
							s1, s2 = sample1, sample2
						if similar[maxsample1][maxsample2] > similar[s1][s2]:
							maxsample1 = s1
							maxsample2 = s2
				if similar[minsample1][minsample2] < similar[maxsample1][maxsample2]:
					minsample1 = maxsample1
					minsample2 = maxsample2
					mini = i
					minj = j

		history.append([minsample2, minsample1])
		group[minj].extend(group[mini])
		group.pop(mini)
		print group

	#描画
	print '\n-----------------------------------------------------------\n'
	dend = []
	pos = NUM * [0]
	count = 0
	text = []
	for i in range(0, len(group)):
		for sample in group[i]:
			dend.append(sample)
			text.append('%2d --'% sample)
			text.append('     ')
			pos[sample] = count
			count += 2

	for his in history:
		if pos[his[0]] > pos[his[1]]:
			his[0], his[1] = his[1], his[0]
		for i in range(0, len(text)):
			if i >= pos[his[0]] and i <= pos[his[1]]:
				text[i] += '|'
			elif pos.count(i) > 0:
				text[i] += '-'
			else:
				text[i] += ' '

		temp = (pos[his[0]] + pos[his[1]]) / 2
		p0 = pos[his[0]]
		p1 = pos[his[1]]

		for i in range(0, history.index(his) + 1):
			if pos[history[i][0]] == p0 or pos[history[i][0]] == p1 or pos[history[i][1]] == p0 or pos[history[i][1]] == p1:
				for h in history[i]:
					pos[h] = temp

		for i in range(0, len(text)):
			if pos.count(i) > 0:
				text[i] += '--'
			else:
				text[i] += '  '

	for line in text:
		print line

