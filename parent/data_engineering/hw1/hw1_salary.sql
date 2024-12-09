
SELECT rsh.person, 
"class",
salary,
effective_from, 
effective_to,
payment,
sp.dt,
coalesce (sum(sp.payment) over (partition by sp.person,rsh.effective_from order by sp.person,rsh.effective_from rows between unbounded preceding and current row) ,0) as month_paid,
rsh.salary - coalesce (sum(sp.payment) over (partition by sp.person,rsh.effective_from order by sp.person,rsh.effective_from rows between unbounded preceding and current row) ,0) as month_rest
FROM de.rvga_salary_hist rsh
join salary_payments sp 
on sp.person=rsh.person 
and sp.dt >= rsh.effective_from 
and sp.dt <= rsh.effective_to 
order by sp.person,sp.dt 
