# -*- coding:utf-8 -*-
#単連結法 凝集型クラスタリング

import MeCab

NUM = 10
GROUP = 3

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
	for i in range(0, NUM):
		group.append([])
		group[i].append(i)
		article[i] = Article('./data/%02d.txt'%i)
		similar[i] = {}
		for j in range(0, i):
			similar[i][j] = article[i].calcSimilar(article[j])

	while len(group) > GROUP:
		mini = 1
		minj = 0
		minsample1 = group[mini][0]
		minsample2 = group[minj][0]

		for i in range(0, len(group)):
			for j in range(0, i):
				for sample1 in group[i]:
					for sample2 in group[j]:
						if sample1 < sample2:
							sample1, sample2 = sample2, sample1
						if similar[minsample1][minsample2] < similar[sample1][sample2]:
							minsample1 = sample1
							minsample2 = sample2
							mini = i
							minj = j
		group[minj].extend(group[mini])
		group.pop(mini)
		print group
