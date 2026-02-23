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
	count(*) AS nb_transactions,
	ROUND(
        100.0 * COUNT(*) / SUM(COUNT(*)) OVER (),
        2
    ) as pourcentage_total
FROM
	transactions 
GROUP BY	
    transaction_type
ORDER BY
    nb_transactions DESC;

--Solde moyen par type de compte--
SELECT
	account_type ,
	ROUND(AVG(account_balance), 2) AS solde_moyen
FROM
	accounts
GROUP BY	
    account_type
ORDER BY
    solde_moyen DESC;

--Détection de transaction anormale--
--j'ai mis 3500 car il y'a pas de transactions qui dépasse 3500 dans la bdd--
SELECT
	transaction_id ,
	account_id,
	transaction_date,
	amount AS transaction_anormale,
	transaction_type
FROM
	transactions 
WHERE
	amount > 3500 ;

