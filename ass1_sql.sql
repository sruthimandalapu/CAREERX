-- Part1:

-- select student.student_id,student.name from student inner join guide on student.phone=guide.student_phone group by student.student_id,student.name having count(guide.guide_id)>1

-- select s1.name,s1.dept from student s1 inner join (select avg(gpa) avg_gpa,dept from student group by dept) s2 on s1.dept=s2.dept where s1.gpa>s2.avg_gpa 

-- select name from student s where gpa=(select max(gpa) from student where dept=s.dept)

-- select s1.name as student1, s1.dept as dept1, s2.name as student2, s2.dept as dept2, g1.guide_name from student s1 join guide g1 on s1.phone = g1.student_phone join student s2 on s1.phone != s2.phone join guide g2 on s2.phone = g2.student_phone and g1.guide_id = g2.guide_id where s1.dept != s2.dept

-- select g.guide_name, g.guide_id, avg(s.gpa) as avg_gpa from guide g join student s on g.student_phone=s.phone group by g.guide_name, g.guide_id order by avg_gpa desc limit 1;

-- select student_id,name from student inner join guide on student.phone=guide.student_phone

-- select g.guide_name from guide g join student s on g.student_phone=s.phone group by g.guide_name having count(distinct s.dept) > 1;

-- select s.name from student s where s.dept in (select distinct s2.dept from guide g join student s2 on g.student_phone= s2.phone where g.guide_name = 'Dr. Jennifer') group by s.name having count(distinct s.dept) = (select count(distinct s3.dept) from guide g2 join student s3 on g2.student_phone= s3.phone where g2.guide_name = 'Dr. Jennifer')

-- select g.guide_name from guide g join student s on g.student_phone= s.phone where s.dept = 'CSE' group by g.guide_name having count(*) = (select max(guide_count) from (select count(*) as guide_count from guide g2 join student s2 on g2.student_phone= s2.phone where s2.dept = 'CSE' group by g2.guide_name) as guide_counts);

-- with ranks as (select s.name, s.dept, s.gpa, row_number() over (partition by s.dept order by s.gpa) as rn, count(*) over (partition by s.dept) as total_count from student s), median_gpa as (select dept, case when total_count % 2 = 1 then max(case when rn = (total_count + 1) / 2 then gpa end) else avg(case when rn in (total_count / 2, total_count / 2 + 1) then gpa end) end as median from ranks group by dept, total_count) select s.name, s.dept from student s join median_gpa mg on s.dept = mg.dept where s.gpa < mg.median;


-- Part2:

-- select * from employees where department='IT';

-- select * from projects where budget>100000;

-- select department, avg(salary) as average_salary from employees group by department;

-- select lead,count(project_name) as number_of_projects from projects group by lead having count(project_name)>1;

-- select * from employees e inner join projects p on p.lead=e.first_name+' '+e.last_name where p.budget>50000 and e.hire_date >= DATEADD(YEAR, -5, GETDATE())

-- insert into employees values(11,'Ron','Doe','Finance',90000,'2023-03-12'),
-- (12,'Jane','Smith','IT',85000,'2020-08-01'),
-- (13,'Michael','Johnson','HR',75000,'2019-07-23')
-- insert into projects values(106,'Zeta','Frank Taylor',85000),
-- (107,'Eta','Grace Lee',100000),
-- (108,'Theta','Henry Martin',90000),
-- (109,'Iota','Irene Harris',150000)
-- select * from employees
-- select * from projects

-- update projects set budget=160000 where project_name='Alpha'
-- select * from projects

-- delete from projects where last_budget_increase>dateadd(year,-3,getdate())
-- select * from projects

-- select * from employees where department='Marketing' and salary>(select AVG(salary) from employees where department='Marketing')

-- select e.* from employees e inner join projects p on e.first_name+' '+e.last_name= p.lead where datediff(day,e.hire_date,getdate())>1095;


-- extra:

-- select * from employee_skills
--with employee_skillsets as(select employee_id,string_agg(Skill, ', ') within group(order by Skill) as Skills,count(distinct Skill) as
--SkillCount from Employee_Skills group by employee_id having count(distinct Skill)>=3) select employee_id,skills from employee_skillsets
--where Skills in(select Skills from employee_skillsets group by Skills having count(*)=1)





