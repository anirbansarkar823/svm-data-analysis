
title: Attributes tagging for Degree college upto to UG.  
date: Thurday 30, May 2019
---

## About the document
This file documents the process and rationale of designating
particular scoring method for the asset 'Degree college upto
UG'.

## Attributes for scoring the asset
* General Information
	- Departments
	- Job Placement
	- Fees
* Organisations
	- Student Union
	- Societies
* Partnerships
	- Affiliations
* Scholarships
	- Scholarship Oppurtunities

## Overall asset scoring
The score for the asset is calculated as,
\[
	\text{score} &= w_{GI} \times GI \\
		     &+ w_{Org} \times Org \\
		     &+ w_{Pr} \times Pr \\
		     &+ w_{Sc} \times Sc.
\]
where,
\[
	GI &= \text{score from general information.} \\
	Org &= \text{score of variable organisations.} \\
	Pr &= \text{score of variable partnerships.} \\
	Sc &= \text{score of variable scholarships.}
\]

## Attributes scoring and the process
### General Information
The general information variable has three sub-paramters, i.e.,
Departments, Job placement, and Fees. The scoring will be
done as follows,
\[
	GI &= w_{Dpts} \times Dpts \\
	   &+ w_{Jps} \times Jps \\
	   &+ w_{Fees} \times Fees.
\]
where,
\[
	Dpts &= \text{score of department variable.} \\
	Jps &= \text{score of job placement variable.} \\
\]

The scoring of sub-paraters are given below.
##### Departments
The input for this variable is a a string containing the
names of the depatment present in the asset. Assuming, we
can separate the department names, we can classify the
departments into the field they are related to.
