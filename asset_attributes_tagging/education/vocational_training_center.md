---
title: Attributes tagging for Vocational Training Center  
date: Thursday, 30 May 2019
---

## About the document
This file documents the process and rationale of designating
particular scoring method for the asset 'Vocational Training
Center'.


## Attributes for scoring the asset
The attributes for the asset is divided into a main variable
which in turn is divided into futher sub-variables. The following
is a tentative list of variables for the asset:-
* General Information:
	- Demand
	- Job Placement
	- Fees
	- Soft Skills
* Infrastructure:
	- Equipment
* Partnerships:
	- Affiliations
	- Placements
## Overall asset scoring
The overall asset scoring equation is as given below,
\[
	\text{Score}_{asset} &= w_{GI} \times GI \\
			     &+ w_{In} \times In \\
			     &+ w_{Pr} \times Pr.
\]
where,
\[
	GI &= \text{score from general information.} \\
	In &= \text{score of infrastructure.} \\
	Pr &= \text{score from partnerships.}
\]
and $w_{GI}$, $w_{In}$ and $w_{Pr}$ are the respective weights.

## Attribute scoring and the process
In this section we will describe each variable, the scoring
method and the justification for the choosen method.

### General Information
The scoring of general information is given as,
\[
	GI &= w_{demand} \times \text{Demand} \\
	   &+ w_{placement} \times \text{Placement} \\
	   &+ w_{fees} \times \text{Fees} \\
	   &+ w_{soft skills} \times \text{Soft Skills}.
\]

#### Demand
*Suggestion*: This should be three input with multiselect option.  

The demand is to score how much the services of an asset is
wished/wanted by the people concerned. The questionare for 
the attribute is a input for the three most sought out course
that is provide in the vocational training center.


##### Scoring
Since, a content of text input can be vague. So, for scoring
we will just use the following criteria:
1. Text input empty:  
If the text input is empty, then we assume that the courses
provide by the vocational training center are of no interest
to the public. Hence, in this case a score of 0 will be given.

2. Text input given:
In this case, we will assume that the courses are of some
relevance and hence a score of 1 will be assigned. Since, the
input may be vague and due to problems in parsing string
containing natural languages, we will not make any further
assumptions.

So the score of demand will be,  
\[ 
	D &= 0, \text{if input empty} \\
          &= 1, \text{if input not emtpy}
\]
where, $D = \text{score of demand}$.

#### Job Placement
This is a binary yes/no type of question. The input will be
either yes or no depending on whether the vocational training
center provides placement or not. The variable describes the
presence/absence of placment and the quality of placement in
the training center.
##### Scoring
Scoring is done as follows,
\[
	S &= 0, \text{if selected no} \\
     	   		&= 1, \text{if selected yes}
\]
where, $S = \text{denotes the presence/absence of placement}$.

If there some placement facilites then score will be based on
the following criterias:
1. The average number of companies that come to the
campus each year:  
We assume that this will be a numeric type question. A numerical
values representing the average number of companies will be
given as input.

[//]: # This should be numeric type question.

A threshhold value will be set. If the input is equal or greater
that the threshold then the asset will have maximum score
for this criteria. 

The score will increase in a non-linear fashion. i.e. score
gaps between consecutive input values will differ depending
on where they lie in the input range. For smaller values, the
gap will be larger. But for larger values the score gaps will
be smaller.

Hence, the scoring equation is given as follows,
\[
	C = (\dfrac{\sqrt{NC}}{\sqrt{threshold}}).
\]
where, $C$ is the score and, $NC$ is the average number of companies
visiting.

2. The percentage of students that get placed:  
*Suggestion*: There should be more choices, so that score could be finegrained  

This is a multiple chocice single select question. There are
three choices available for ranges in terms of percentage
students that get placed. The score for each choice is given
below.
	Placement percentage | score | Description
	---------------------|-------|------------
	0-25%		     | 0.20  | Good score
	25-50%		     | 0.70  | Better Score
	>50%		     | 1.00  | Best Score

The overall score for job placement variable is given as follows,
\[
	J = S \times (w_c \times C | w_p \times P).
\]
where,
\[
	S &= \text{value for selected.} \\
	C &= \text{score for average companies visiting.} \\
	P &= \text{score for student placement.} \\
	w_c &= \text{weight for companies visiting.} \\
	w_p &= \text{weight for student placement.} \\
	J &= \text{Score for job placement variable.}
\]

#### Fees
The input to this variable will be numerical, specifying the
average fee per student.
##### Scoring
The score for fees will decrease as the fees amount goes high.
The score will be 0 (minimum value) if the fee amount crosses
a certain threshold. Also, score will be 1 (maximum value) if 
the training center doesn't require any fees.

The scoring equations are given as below,
\[
	F &= 0, \text{If fee amount > threshold} \\
	  &= 1, \text{If fee amount = 0} \\
	  &= \dfrac{1}{fee amount}
\]
where, $F = \text{Score for fees}$.

#### Soft Skills
This variable describes the presence/absence of teaching of
soft skills/IT traiing available in the institute. It is a
multiple type binary yes/no question.

This contains a sub-parameter for the influence of private
partners in training.

##### Scoring
The scoring equation is given as below,
\[
	S &= 0, \text{if no soft skill/IT training is present.} \\
	  &= 1, \text{if some soft skill/IT training is present.}
\]
where, $S = \text{score for presence or absence.}

For the sub-parameter representing the involvement of private
partners, we have the following score equation,
\[
	Pr &= 0, \text{no involvement of private partners.} \\
	   &= 1, \text{some involvement of private partners.}
\]

The overall scoring for soft skills variable is done as,
\[
	SS &= \dfrac{S+Pr}{2}.
\]

### Infrastructure
In this section we will discuss the scoring for the insfracture
facilities of the asset. The asset has only one variable for
infrastructure. The scoring is done as follows.
\[
	I = \text{Equipment Score}.
\]
where, $I = \text{Score for Infrastructure.}$
#### Equipment
For equipment we have only one question. If the equipment present
in the asset is adequate then we will get yes as input and no if not.

Hence, scoring equation is given below,
\[
	E &= 0, \text{If yes is selected.} \\
	  &= 1, \text{If no is selected.}
\]

### Partnerships
This is a variable for measuring the amount and quality of
collaboration happening between the institute of insterest
and other government/non-government bodies.

The scoring equation is given as,
\[
	PS &= w_{affiliations} \times \text{Affiliations} \\
	   &+ w_{placement} \times \text{Placementi.}
\]

The scoring of individual sub-parameters are given in the
sections below.
#### Affiliations
*Suggestion*: This should be a binary yes/no question.  

The input to this sub-parameter is text describing the affiliations
of the asset with other institutions. Since, textual input
can be ambiguous. So, we will score as follows.
1. If text input present. score will be 1.
2. If text input empty. score will be 0.

So, the scoring is as follows,
\[
	A &= 0, \text{if input empty.} \\
	  &= 1, \text{if input not empty.}
\]

#### Placement
This variable represents the presence/absence of partnerships
with other institutes for placement. Hence, it is a binary
yes/no question. Scoring is done as follows.
\[
	P &= 0, \text{partnership with other institutes absent.} \\
	  &= 1, \text{partnership with other institutes present.}
\]
