# Additional Queries

Ad-hoc queries ran for data visualization purposes and additional data quality issues.

### Create view of cap-code pivot table

```sql
create or replace view
  cap_code_pivot as
select
  b.cap_code,
  coalesce(b.count,0) as bill_count,
  coalesce(n.count,0) as news_count
from
  (
    select
      cap_code,
      count(number) as count
    from
      bill
    group by
      cap_code
  ) as b
  left outer join (
    select
      cap_code,
      count(article_id) as count
    from
      news
    group by
      cap_code
  ) as n on b.cap_code = n.cap_code;
```

Here I created a view from both `news` and `bill` that allowed me to cross compare how many of each cap code each database has at the moment.

A subset of the results look like:

|cap_code|bill_count|news_count|
|--------|----------|----------|
|Agriculture|1|0|
|Law and Crime|1|7|
|International Affairs|1|22|
|Energy|4|0|

The table in my Superset screenshot just is this table

### Update News Source

```sql
update news
set
source = substring(title from '[a-zA-Z|\d][^-]*$')
```

I realized that the `source` of my `news` was all wrong. While I updated my Python code to pull from the `<source>` tag, I needed to fix current data. I used a regular expression to pull out the last few characters in the `title` that started with an alphacharacter and was anything other than a hyphen. This consistently pulled the `source` from the title because of how Google New's titles are compiled.


### update_date

Even though the Library of Congress publishes the `IntroducedDate` of each bill, I didn't initially export that data. In [update_date.py](update_date.py), I wrote a statement that added the appropriate column:

```sql
ALTER TABLE bill
ADD COLUMN IF NOT EXISTS introduced_date date
```

then wrote a query that returned the bill's url from all rows with a `NULL` date:

```sql
SELECT number, url
FROM bill
WHERE introduced_date IS NULL
```

got the introduced date with Python, and then updated each row as appropriate:

```sql
UPDATE bill
SET introduced_date = {date}
WHERE number = {number}
```
