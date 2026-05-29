% ============================================================
% Smart Interview Preparation Expert System
% Prolog Knowledge Base
% Demonstrates: Knowledge Representation, Rule-Based Reasoning,
%               Backward Chaining, and Unification
% ============================================================


% ============================================================
% SECTION 1: ROLE DEFINITIONS
% Represents what each job role requires (knowledge representation)
% ============================================================

role(software_engineer).
role(web_developer).
role(data_analyst).
role(ui_ux_designer).

% ============================================================
% SECTION 2: SKILL REQUIREMENTS PER ROLE
% required_skill(Role, Skill)
% This forms the knowledge base for backward chaining
% ============================================================

required_skill(software_engineer, python).
required_skill(software_engineer, dsa).
required_skill(software_engineer, oop).
required_skill(software_engineer, sql).
required_skill(software_engineer, git).

required_skill(web_developer, html_css).
required_skill(web_developer, javascript).
required_skill(web_developer, git).
required_skill(web_developer, oop).
required_skill(web_developer, sql).

required_skill(data_analyst, python).
required_skill(data_analyst, sql).
required_skill(data_analyst, statistics).
required_skill(data_analyst, excel).
required_skill(data_analyst, visualization).

required_skill(ui_ux_designer, html_css).
required_skill(ui_ux_designer, figma).
required_skill(ui_ux_designer, user_research).
required_skill(ui_ux_designer, prototyping).
required_skill(ui_ux_designer, javascript).


% ============================================================
% SECTION 3: SKILL IMPORTANCE WEIGHTS
% skill_weight(Role, Skill, Weight)
% Weight: high / medium / low
% Used for readiness scoring
% ============================================================

skill_weight(software_engineer, dsa,    high).
skill_weight(software_engineer, python, high).
skill_weight(software_engineer, oop,    high).
skill_weight(software_engineer, sql,    medium).
skill_weight(software_engineer, git,    medium).

skill_weight(web_developer, javascript, high).
skill_weight(web_developer, html_css,   high).
skill_weight(web_developer, oop,        medium).
skill_weight(web_developer, sql,        medium).
skill_weight(web_developer, git,        medium).

skill_weight(data_analyst, sql,           high).
skill_weight(data_analyst, python,        high).
skill_weight(data_analyst, statistics,    high).
skill_weight(data_analyst, excel,         medium).
skill_weight(data_analyst, visualization, medium).

skill_weight(ui_ux_designer, figma,         high).
skill_weight(ui_ux_designer, user_research, high).
skill_weight(ui_ux_designer, html_css,      medium).
skill_weight(ui_ux_designer, prototyping,   medium).
skill_weight(ui_ux_designer, javascript,    medium).


% ============================================================
% SECTION 4: WEAK SKILL DETECTION (Backward Chaining)
% is_weak_skill(Role, Skill, UserSkills)
% Succeeds if Skill is required for Role but NOT in UserSkills
% This uses Prolog's built-in negation-as-failure (\+)
% ============================================================

is_weak_skill(Role, Skill, UserSkills) :-
    required_skill(Role, Skill),          % Skill is required for Role
    \+ member(Skill, UserSkills).         % Skill is NOT in user's skill list


% ============================================================
% SECTION 5: ALL WEAK SKILLS FOR A ROLE
% weak_skills(Role, UserSkills, WeakSkills)
% Collects all skills the user is missing for the given role
% Uses findall for exhaustive backward chaining
% ============================================================

weak_skills(Role, UserSkills, WeakSkills) :-
    findall(Skill, is_weak_skill(Role, Skill, UserSkills), WeakSkills).


% ============================================================
% SECTION 6: RECOMMENDATION RULES
% recommend(Role, Skill, Recommendation)
% Provides specific preparation advice per skill and role
% Demonstrates rule-based expert reasoning
% ============================================================

recommend(software_engineer, dsa,    'Practice LeetCode problems; focus on arrays, trees, and graphs').
recommend(software_engineer, python, 'Review Python fundamentals: data structures, OOP, and libraries').
recommend(software_engineer, oop,    'Study OOP concepts: encapsulation, inheritance, polymorphism, abstraction').
recommend(software_engineer, sql,    'Practice SQL queries: joins, subqueries, and aggregation').
recommend(software_engineer, git,    'Learn Git: branching, merging, pull requests, and conflict resolution').

recommend(web_developer, javascript, 'Master JavaScript: ES6+, async/await, DOM manipulation').
recommend(web_developer, html_css,   'Strengthen HTML5 semantics and CSS layouts (Flexbox, Grid)').
recommend(web_developer, oop,        'Learn OOP patterns commonly used in JavaScript and web frameworks').
recommend(web_developer, sql,        'Study relational databases and SQL for backend integration').
recommend(web_developer, git,        'Practice Git workflows used in team-based web development').

recommend(data_analyst, sql,           'Master complex SQL: window functions, CTEs, and optimization').
recommend(data_analyst, python,        'Focus on Python for data analysis: Pandas, NumPy, and Matplotlib').
recommend(data_analyst, statistics,    'Review statistics: distributions, hypothesis testing, and regression').
recommend(data_analyst, excel,         'Practice Excel: pivot tables, VLOOKUP, and data visualization').
recommend(data_analyst, visualization, 'Learn Tableau or Power BI for professional data visualization').

recommend(ui_ux_designer, figma,         'Master Figma: components, auto-layout, and prototyping features').
recommend(ui_ux_designer, user_research, 'Study user research methods: surveys, usability testing, interviews').
recommend(ui_ux_designer, html_css,      'Learn basic HTML/CSS to collaborate effectively with developers').
recommend(ui_ux_designer, prototyping,   'Build interactive prototypes using Figma or Adobe XD').
recommend(ui_ux_designer, javascript,    'Understand JavaScript basics for design-to-code communication').


% ============================================================
% SECTION 7: GET ALL RECOMMENDATIONS
% get_recommendations(Role, WeakSkills, Recommendations)
% Unifies each weak skill with its recommendation
% ============================================================

get_recommendations(_, [], []).
get_recommendations(Role, [Skill|Rest], [rec(Skill, Rec)|Recs]) :-
    recommend(Role, Skill, Rec),
    get_recommendations(Role, Rest, Recs).
get_recommendations(Role, [_|Rest], Recs) :-
    get_recommendations(Role, Rest, Recs).


% ============================================================
% SECTION 8: READINESS SCORE CALCULATION
% readiness_score(Role, UserSkills, Confidence, Experience, Score)
% Score is calculated out of 100 using weighted skill coverage
% Confidence and experience also influence the score
% ============================================================

% Point values for skill weights
weight_score(high,   30).
weight_score(medium, 20).
weight_score(low,    10).

% Confidence level adjustments
confidence_bonus(high,   10).
confidence_bonus(medium,  5).
confidence_bonus(low,     0).

% Experience level adjustments
experience_bonus(senior, 10).
experience_bonus(mid,     5).
experience_bonus(junior,  0).
experience_bonus(fresher, 0).

% Calculate total possible points for a role
total_possible_points(Role, Total) :-
    findall(W,
        (required_skill(Role, Skill),
         skill_weight(Role, Skill, Level),
         weight_score(Level, W)),
        Weights),
    sumlist(Weights, Total).

% Calculate earned points from user's skills
earned_points(Role, UserSkills, Earned) :-
    findall(W,
        (required_skill(Role, Skill),
         member(Skill, UserSkills),
         skill_weight(Role, Skill, Level),
         weight_score(Level, W)),
        Weights),
    sumlist(Weights, Earned).

% Final readiness score (0-100)
readiness_score(Role, UserSkills, Confidence, Experience, Score) :-
    total_possible_points(Role, Total),
    earned_points(Role, UserSkills, Earned),
    Total > 0,
    BaseScore is (Earned * 80) // Total,
    confidence_bonus(Confidence, CB),
    experience_bonus(Experience, EB),
    RawScore is BaseScore + CB + EB,
    Score is min(RawScore, 100).


% ============================================================
% SECTION 9: READINESS CATEGORY RULES
% readiness_category(Score, Category)
% Classifies readiness level based on score ranges
% ============================================================

readiness_category(Score, 'Interview Ready') :-
    Score >= 80, !.
readiness_category(Score, 'Almost Ready') :-
    Score >= 60, Score < 80, !.
readiness_category(Score, 'Needs Preparation') :-
    Score >= 40, Score < 60, !.
readiness_category(_, 'Significant Preparation Required').


% ============================================================
% SECTION 10: HIGH-PRIORITY SKILLS
% high_priority_weak(Role, WeakSkills, HighPriorityWeak)
% Identifies high-importance weak skills to focus on first
% ============================================================

high_priority_weak(Role, WeakSkills, HighPriorityWeak) :-
    findall(Skill,
        (member(Skill, WeakSkills),
         skill_weight(Role, Skill, high)),
        HighPriorityWeak).


% ============================================================
% SECTION 11: ROLE MATCH CHECK
% role_match(Role, UserSkills, MatchPercent)
% Calculates how well a user's skills match a given role
% ============================================================

role_match(Role, UserSkills, MatchPercent) :-
    findall(S, required_skill(Role, S), AllRequired),
    length(AllRequired, Total),
    Total > 0,
    findall(S, (required_skill(Role, S), member(S, UserSkills)), Matched),
    length(Matched, MatchedCount),
    MatchPercent is (MatchedCount * 100) // Total.


% ============================================================
% SECTION 12: ALTERNATIVE ROLE SUGGESTIONS
% suggest_alternative_role(UserSkills, SuggestedRole, MatchPct)
% Finds roles where user already has the most matching skills
% ============================================================

suggest_alternative_role(UserSkills, SuggestedRole, MatchPct) :-
    findall(Pct-R,
        (role(R), role_match(R, UserSkills, Pct)),
        Pairs),
    msort(Pairs, Sorted),
    last(Sorted, MatchPct-SuggestedRole).


% ============================================================
% HELPER PREDICATES
% ============================================================

% sumlist/2 - sums a list of numbers
sumlist([], 0).
sumlist([H|T], Sum) :-
    sumlist(T, Rest),
    Sum is H + Rest.

% last/2 - gets last element of list
last([X], X).
last([_|T], X) :- last(T, X).
