import json

models = {'courses.course': [{'model': 'courses.course', 'pk': 2, 'fields': {'instructor': 1, 'subject': 2, 'title': 'Math 225', 'overview': 'Logic is the formal science of using reason and is considered a branch of both philosophy and mathematics and to a lesser extent computer science.', 'slug': 'math-225', 'created': '2021-12-10T13:54:23.239Z', 'feature': False, 'photo': 'courses/2021/12/11/logic-homework-1416930.jpg'}}, {'model': 'courses.course', 'pk': 3, 'fields': {'instructor': 1, 'subject': 2, 'title': 'Stat 200', 'overview': 'Statistics is a field of inquiry that studies the collection, analysis, interpretation, and presentation of data. It is applicable to a wide variety of academic disciplines.', 'slug': 'stat-200', 'created': '2021-12-10T13:56:08.947Z', 'feature': False, 'photo': 'courses/2021/12/11/bar-graph-1165986_uwYBPYC.jpg'}}], 'courses.module': [{'model': 'courses.module', 'pk': 2, 'fields': {'course': 3, 'title': 'Inferential statistics', 'description': 'Statistical inference is the process of using data analysis to deduce properties of an underlying probability distribution.', 'order': 1}}, {'model': 'courses.module', 'pk': 3, 'fields': {'course': 3, 'title': 'Exploratory data analysis', 'description': 'Exploratory data analysis (EDA) is an approach to analyzing data sets to summarize their main characteristics, often with visual methods.', 'order': 2}}], 'courses.content': [{'model': 'courses.content', 'pk': 3, 'fields': {'module': 1, 'content_type': 13, 'object_id': 1, 'order': 1}}, {'model': 'courses.content', 'pk': 4, 'fields': {'module': 1, 'content_type': 10, 'object_id': 1, 'order': 2}}, {'model': 'courses.content', 'pk': 5, 'fields': {'module': 1, 'content_type': 14, 'object_id': 1, 'order': 3}}, {'model': 'courses.content', 'pk': 6, 'fields': {'module': 2, 'content_type': 10, 'object_id': 2, 'order': 1}}, {'model': 'courses.content', 'pk': 7, 'fields': {'module': 2, 'content_type': 14, 'object_id': 2, 'order': 2}}, {'model': 'courses.content', 'pk': 8, 'fields': {'module': 2, 'content_type': 11, 'object_id': 3, 'order': 0}}, {'model': 'courses.content', 'pk': 9, 'fields': {'module': 2, 'content_type': 13, 'object_id': 2, 'order': 3}}, {'model': 'courses.content', 'pk': 10, 'fields': {'module': 3, 'content_type': 11, 'object_id': 4, 'order': 1}}, {'model': 'courses.content', 'pk': 11, 'fields': {'module': 3, 'content_type': 13, 'object_id': 3, 'order': 2}}, {'model': 'courses.content', 'pk': 12, 'fields': {'module': 3, 'content_type': 10, 'object_id': 3, 'order': 0}}], 'courses.text': [{'model': 'courses.text', 'pk': 3, 'fields': {'instructor': 1, 'title': 'Note', 'created': '2021-12-11T09:41:42.600Z', 'updated': '2021-12-11T09:41:42.600Z', 'content': '<p><u><strong>A descriptive statistic</strong></u> (in the count noun sense) is a summary statistic that quantitatively describes or summarizes features from a collection of information,[1] while descriptive statistics (in the mass noun sense) is the process of using and analysing those statistics. Descriptive statistics is distinguished from inferential statistics (or inductive statistics) by its aim to summarize a sample, rather than use the data to learn about the population that the sample of data is thought to represent.[2]</p>\r\n\r\n<p>This generally means that <span style="color:#c0392b"><strong>descriptive statistics, unlike inferential statistics, is not developed on the basis of probability theory,</strong></span> and are frequently non-parametric statistics.[3] Even when a data analysis draws its main conclusions using inferential statistics, descriptive statistics are generally also presented.[4] For example, in papers reporting on human subjects, typically a table is included giving the overall sample size, sample sizes in important subgroups (e.g., for each treatment or exposure group), and demographic or clinical characteristics such as the average age, the proportion of subjects of each sex, the proportion of subjects with related co-morbidities, etc.</p>\r\n\r\n<p>Some measures that are commonly used to describe a data set are measures of central tendency and measures of variability or dispersion.</p>\r\n\r\n<p>Measures of central tendency include the mean, median and mode, while measures of variability include the standard deviation (or variance), the minimum and maximum values of the variables, kurtosis and skewness.[</p>'}}, {'model': 'courses.text', 'pk': 4, 'fields': {'instructor': 1, 'title': 'Note', 'created': '2021-12-11T09:47:27.696Z', 'updated': '2021-12-11T09:47:27.696Z', 'content': '<h1><u><strong>Introduction</strong></u></h1>\r\n\r\n<p>In statistics, <strong>exploratory data analysis </strong>is an approach of analyzing data sets to summarize their main characteristics, often using statistical graphics and other data visualization methods. A statistical model can be used or not, but primarily EDA is for seeing what the data can tell us beyond the formal modeling or hypothesis testing task.</p>\r\n\r\n<hr />\r\n<p>Exploratory data analysis has been promoted by John Tukey since 1970 to encourage statisticians to explore the data, and possibly formulate hypotheses that could lead to new data collection and experiments. EDA is different from initial data analysis (IDA), which focuses more narrowly on checking assumptions required for model fitting and hypothesis testing, and handling missing values and making transformations of variables as needed. EDA encompasses IDA.</p>\r\n\r\n<hr />\r\n<h1><u><strong>Overview</strong></u></h1>\r\n\r\n<p>Tukey defined data analysis in 1961 as: &quot;Procedures for analyzing data, techniques for interpreting the results of such procedures, ways of planning the gathering of data to make its analysis easier, more precise or more accurate, and all the machinery and results of (mathematical) statistics which apply to analyzing data.&quot;[2]</p>\r\n\r\n<p>&nbsp;</p>\r\n\r\n<p>Tukey&#39;s championing of EDA encouraged the development of statistical computing packages, especially S at Bell Labs. The S programming language inspired the systems S-PLUS and R. This family of statistical-computing environments featured vastly improved dynamic visualization capabilities, which allowed statisticians to identify outliers, trends and patterns in data that merited further study.</p>\r\n\r\n<p>&nbsp;</p>\r\n\r\n<p>Tukey&#39;s EDA was related to two other developments in statistical theory: robust statistics and nonparametric statistics, both of which tried to reduce the sensitivity of statistical inferences to errors in formulating statistical models. Tukey promoted the use of five number summary of numerical data&mdash;the two extremes (maximum and minimum), the median, and the quartiles&mdash;because these median and quartiles, being functions of the empirical distribution are defined for all distributions, unlike the mean and standard deviation; moreover, the quartiles and median are more robust to skewed or heavy-tailed distributions than traditional summaries (the mean and standard deviation). The packages S, S-PLUS, and R included routines using resampling statistics, such as Quenouille and Tukey&#39;s jackknife and Efron&#39;s bootstrap, which are nonparametric and robust (for many problems).</p>'}}], 'courses.image': [{'model': 'courses.image', 'pk': 2, 'fields': {'instructor': 1, 'title': 'Resource', 'created': '2021-12-11T09:42:06.266Z', 'updated': '2021-12-11T09:42:06.266Z', 'file': 'images/inferential_stat_nudI1A6.png'}}, {'model': 'courses.image', 'pk': 3, 'fields': {'instructor': 1, 'title': 'Resources (image)', 'created': '2021-12-11T09:48:27.936Z', 'updated': '2021-12-11T09:48:27.936Z', 'file': 'images/statics_ml_VBSk6jQ.png'}}], 'courses.video': [{'model': 'courses.video', 'pk': 2, 'fields': {'instructor': 1, 'title': 'Lecture', 'created': '2021-12-11T09:39:32.359Z', 'updated': '2021-12-11T09:39:32.359Z', 'url': 'https://www.youtube.com/watch?v=eOj5dwV4hbU'}}, {'model': 'courses.video', 'pk': 3, 'fields': {'instructor': 1, 'title': 'Lecture', 'created': '2021-12-11T09:49:26.067Z', 'updated': '2021-12-11T09:49:26.067Z', 'url': 'https://www.youtube.com/watch?v=9m4n2xVzk9o'}}]}

# with open('./courses/fixtures/courses.json','r') as data:
#     data = json.loads(data.read())
#     instructors = []
#     for model in data:
#         if model['model'] in ['courses.course','courses.module','courses.content','courses.text','courses.image','courses.video']:
#             if model['model'] not in models:
#                 models[model['model']] = []
#             else:
#                 models[model['model']].append(model)
# print(models)
# data = json.load(str(data))
# print(data)
