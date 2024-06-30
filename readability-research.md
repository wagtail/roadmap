# Review state of the art research papers about readability formulas


## Common readability scales
- Flesch Reading Ease
- Flesch–Kincaid Grade Level
- Automated Readability Index
- New Dale–Chall Readability Formula
- Advantage-TASA Open Standard (commercial)
- Lexile (commercial)
- Pearson Reading Maturity Metric (commercial)
- TextEvaluator Tool (commercial)


## Paper 1: A large-scaled corpus for assessing text readability

>[!info] Key facts
>Year: 2022
>Citations: 20

*Crossley, S., Heintz, A., Choi, J.S. et al. A large-scaled corpus for assessing text readability. Behav Res **55**, 491–507 (2023). https://doi.org/10.3758/s13428-022-01802-x*

> [!Abstract] This paper: 
> - Introduces the CommonLit Ease of Readability (CLEAR) corpus, which provides unique readability scores for ~ 5000 text excerpts along with information about the excerpt’s year of publishing, genre, and other metadata.
> - Discusses the development of the corpus and presents reliability metrics for the human ratings of readability.
>  - Notes existing readability formulas used for educational texts, and argues they are problematic. 


### Key points
- Traditional readability formulas (such as Flesch Reading Ease, Flesch–Kincaid Grade Level and New Dale–Chall Readability Formula) focus on text comprehension rather than text processing, rely on proxies, and are based on small corpora or texts from esoteric domains
- A number of studies have found NLP-informed readability formulas - both commercial and open source - to be more reliable than traditional formulas, notably across a variety of texts

### Limitations of traditional readability formulas
- "most research into text readability is more focused on measuring text understanding (i.e., comprehension Kate et al., [2010](https://link.springer.com/article/10.3758/s13428-022-01802-x#ref-CR46 "Kate, R., Luo, X., Patwardhan, S., Franz, M., Florian, R., Mooney, R., Roukos, S., & Welty, C (2010). Learning to predict readability using diverse linguistic features. In: Proceedings of the 23rd International Conference on Computational Linguistics, (pp. 546–554). Association for Computational Linguistics.")) and not the speed at which a text is read (i.e., text processing)"
- "traditional readability formulas rely on proxy estimates for lexical and syntactic features. For example, number of characters per word is used as a proxy for word sophistication, and number of words per sentence is used as a proxy for syntactic complexity"
- "traditional formulas often ignore concerns of style, vocabulary, and grammar, which may equally play a role in text readability"
- "the reading criteria used to develop traditional formulas are often based on multiple-choice questions and cloze tests, two methods that may not measure text comprehension accurately"
- "most traditional readability formulas [...] have been normed using readers from specific age groups and using small corpora of texts from specific domains."
	- The Flesch Reading Ease formula (Flesch, [1948](https://link.springer.com/article/10.3758/s13428-022-01802-x#ref-CR30 "Flesch, R. (1948). A new readability yardstick. Journal of Applied Psychology, 32(3), 221–233.")) and the Dale–Chall formula (Dale & Chall, [1948](https://link.springer.com/article/10.3758/s13428-022-01802-x#ref-CR25 "Dale, E., & Chall, J. S. (1948). A formula for predicting readability: Instructions. Educational Research Bulletin, 37–54.")) are both based on 350 texts from the 1920s for 3rd through 12th graders
	- The Flesch Kincaid Grade Level formula was based on a small corpus from Navy training materials

### CLEAR
- Collaboration between CommonLit, a non-profit education technology organization focused on improving reading, writing, communication, and problem-solving skills, and Georgia State University (GSU)
- Its objective is to promote the development of more advanced and open-source readability formulas, particularly for use by government agencies in testing, materials selection and creation, and more. 
- CLEAR provides unique readability scores for ~ 5000 text excerpts along with information about the excerpt’s year of publishing, genre, and other metadata.

#### Advantages of CLEAR
- Large - Much larger than any available corpora that provide readability criterion based on human judgement. Other large corpora (such as Newsela) do not provide readability criterion for individual texts, and corpora that do are much smaller (N = ~60-200 texts)
- Broad - Curated from texts available through CommonLit, which selected excerpts from Wikipedia, Project Gutenberg, and other digital libraries. The text excerpts were also published over a very long period of time (1791 - 2020). 
- Texts were hand-selected and hand-edited, ensuring high quality and minimal errors. 
- The CLEAR corpus also includes metadata which provides opportunity for subanalyses. 

#### Limitations of CLEAR
- Readability criteria are based on judgements from schoolteachers about how difficult the excerpts would be for their students to read. 


## Paper 2: # Perusal of readability with focus on web content understandability

>[!INFO] Key facts
>Year: 2021
>Citations:  18

*Pawan Kumar Ojha, Abid Ismail, Kuppusamy Kundumani Srinivasan,
Perusal of readability with focus on web content understandability, Journal of King Saud University - Computer and Information Sciences, Volume 33, Issue 1, 2021, Pages 1-10, ISSN 1319-1578,
https://doi.org/10.1016/j.jksuci.2018.03.007.*

>[!tldr] This paper:
> - Analyzes the popular readability indices used to check the readability of websites and web pages
> - Makes suggestions, based on survey findings, to consider while developing readability formulas

### Conclusion / Findings
- Most work on readability formulas still focuses on English only and will not work on texts in scripts other than used by English
	- Most formulas estimate readability in terms of the US grading system 
	- Formulas that focus on non-English languages include Djoko formula (Indonesian), Fernandez Huerta Index (Spanish), Kandal and Moles Index (French) and Al-Heeti (Arabic)
- One limitation of formulas that mostly consider linguistic factors such as length and count of work is that this method could also score high on nonsense text
- Readability methods developed using statistical language modeling may not be suitable for analyzing web content due to the presence of noise such as sidebar menus - when traditional formulas were used to analyze web content, they performed poorly
- There is a lack of research discussing understandability of text for people with disabilities
- Suggested measures to incorporate in improved readability formulas include: 
	- structural components of the web such as hyperlinks and alt text
	- weighting content - for example level 1 headings being weighted higher
	- considering how to deal with dynamic content such as text within a collapsible element


## Paper 3: # Towards Techniques for Easy-to-Read Web Content

>[!info] Key facts:
>Year: 2014
>Citations: 12

*Annika Nietzio, Daniel Naber, Christian Bühler, Towards Techniques for Easy-to-Read Web Content, Procedia Computer Science, Volume 27, 2014, Pages 343-349, ISSN 1877-0509, https://doi.org/10.1016/j.procs.2014.02.038.*

>[!Abstract] This paper:
>- Compares approaches to check understandability of web content
>- Describes a method to extend coverage of tools across multiple languages

### Key points
- Clear language of content as well as its structure and presentation are equally important in supporting the user in finding, understanding and using the information on the web
- Assessing the readability of content can be achieved by asking readers for feedback if the audience is known, but for web content it can be difficult to identify a representative sample, and results are not reproducible
- Readability indices are a quantitative approach that produce a single number that can be produced automatically, and results are reproducible
- While there are many indices developed for general text, none exist specifically for web content
- Principles for writing easy to read (E2R) text may conflict with how readability indices score text. 
	- For example, E2R recommends repeating noun phrases instead of using pronouns to make it clear who is doing what, but using more words may result in a lower score from traditional readability indices
- Basic spell checking software typically do not cover readability, though increasingly commercial software is emerging that supports authors in producing plain language
- The [European *Information for all* guidelines](https://www.inclusion-europe.eu/easy-to-read-standards-guidelines/) are a set of standards aiming to make information easy to read and understand and contain a set of rules for twelve European languages
	- The rules cover audience, linguistic properties, as well as layout and presentation

### Conclusion / Findings
- Language-independent aspects of readability must also be considered, such as presentation and interaction on the web, which may have a particular impact on the readability of content for people with disabilities

## Article: Readability Formulas: seven reasons to avoid them and what to do instead

*Not a paper but an article from a UX and usability context.*
https://www.effortmark.co.uk/readability-formulas-seven-reasons-to-avoid-them-and-what-to-do-instead/

- Most readability formulas focus on long sentences and long words, which are helpful principles for readability but not enough by themselves.
- Traditional readability formulas perform differently on the same texts, making their reliability questionable
- Legibility and readability are different - readability also needs to mesure understandability based on things that are difficult for a formula to ascertain, such as logical flow of content and visual aids such as tables or charts that can help comprehension
- Counting word length does not consider whether the audience are likely to know what a word means - while some readability formulas (such as Dale-Chall) use a word list, many of these are outdated and do not consider modern usages, such as *cookie* in a web context
- Functional literacy is more important than grade level - adults with lower reading levels have come to know more words from life experience, so while "promise money" might score better than "security deposit", in real terms, the latter is more understood in real world contexts
- Readability formulas are designed for long-form content will full sentences and paragraphs, so are not fit for purpose for the web, for interactions such as UI labels and web forms. Lists are a common way to make web content easy to read and understand, but would probably score low based on readability formulas.


