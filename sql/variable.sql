-- Retorna o valor medio de financiamento por financiador
SELECT F.nome, AVG(FI.valor) AS valor_medio_financiamento 
FROM FINANCIAMENTO FI 
JOIN FINANCIADOR F ON FI.id_financiador = F.id_financiador 
JOIN PROJETO_DE_PESQUISA PP ON FI.id_projeto_pesq = PP.id_projeto_pesq 
GROUP BY F.nome 
ORDER BY valor_medio_financiamento;