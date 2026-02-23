-- Volume (nombre) de transactions par mois
SELECT
    date_trunc('month', transaction_date) AS month,
    COUNT(*) AS nb_transactions
FROM transactions
GROUP BY date_trunc('month', transaction_date)
ORDER BY month;

--Nombre de transactions par type--
SELECT
	transaction_type ,
	count(*) AS nb_transactions
FROM
	transactions 
GROUP BY	
    transaction_type
ORDER BY
    nb_transactions DESC;

