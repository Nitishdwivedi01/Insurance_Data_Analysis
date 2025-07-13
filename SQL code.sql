CREATE database insurance_data_analysis;
USE insurance_data_analysis;

CREATE TABLE insurance_policies (
    Policy_ID VARCHAR(20),
    Customer_ID VARCHAR(20),
    Policy_Type VARCHAR(20),
    Premium_Amount BIGINT,
    Coverage_Amount FLOAT,
    Policy_Start_Date DATE,   -- Formate should be YYYY-MM-DD for all the dates
    Policy_End_Date DATE,
    Payment_Frequency VARCHAR(20),
    Policy_Status VARCHAR(20),
    Customer_Age INT,
    Customer_Gender VARCHAR(10),
    Customer_Location VARCHAR(100),
    State VARCHAR(50),
    Sales_Agent_ID VARCHAR(20),
    Sales_Channel VARCHAR(20),
    Sale_Date DATE,
    Financial_Year VARCHAR(10),
    Has_Claimed BOOLEAN,
    Claim_Amount BIGINT
);



-- Used python to upload data in the data base and now we will preform our queries 
-- Test query
SELECT * FROM insurance_policies limit 20;

-- Now we will work with the questions and the queries
-- Count of policies that has been claimed and not claimed in all the states 

SELECT 
    State,
    COUNT(*) AS Total_Policies,
    SUM(CASE WHEN Has_Claimed = TRUE THEN 1 ELSE 0 END) AS Claimed_Policies,
    SUM(CASE WHEN Has_Claimed = FALSE THEN 1 ELSE 0 END) AS Unclaimed_Policies
FROM insurance_policies
GROUP BY State
ORDER BY Total_Policies DESC;

select State, count(Policy_ID) AS Total_Policy FROM insurance_policies where Has_claimed = TRUE group by State ORDER BY Total_Policy DESC;

-- Analyze the total premium amount and number of policies sold each financial year
SELECT 
    Financial_Year,
    COUNT(Policy_ID) AS Total_Policy,
    SUM(Premium_Amount) AS Total_Premium
FROM
    insurance_policies
GROUP BY Financial_Year;
 
-- Identify the most popular policy types and their contribution to total premiums
SELECT 
    Policy_Type, SUM(Premium_Amount) AS Total_Premium
FROM
    insurance_policies
GROUP BY Policy_Type;
 
-- Examine sales trends across different policy types over the three financial years
SELECT 
    Financial_Year, Policy_Type, COUNT(Policy_ID)
FROM
    insurance_policies
GROUP BY Financial_Year , Policy_Type
ORDER BY Financial_Year , Policy_Type;

-- Understand the age distribution of policyholders and how age influence policy purchases and premium amounts.
SELECT 
  CASE 
        WHEN Customer_Age BETWEEN 18 AND 24 THEN '18-24'
        WHEN Customer_Age BETWEEN 25 AND 34 THEN '25-34'
        WHEN Customer_Age BETWEEN 35 AND 44 THEN '35-44'
        WHEN Customer_Age BETWEEN 45 AND 54 THEN '45-54'
        WHEN Customer_Age BETWEEN 55 AND 64 THEN '55-64'
	WHEN Customer_Age BETWEEN 65 AND 74 THEN '65-74'
        WHEN Customer_Age >= 75 THEN '70+'
    ELSE 'Unknown'
  END AS Age_Group,
  COUNT(*) AS Total_Customers, sum(Premium_Amount) as Total_Premium
FROM insurance_policies
GROUP BY Age_Group
ORDER BY Age_Group;  
 
 -- Explore how gender influence on policy purchases and premium amounts.
 SELECT 
    Customer_Gender,
    COUNT(Policy_ID) AS Total_Policy,
    SUM(Premium_Amount) AS Total_Premium
FROM
    insurance_policies
GROUP BY Customer_Gender
ORDER BY Customer_Gender;

-- Investigate geographical sales distribution (Customer_Location).
SELECT 
    State,
    COUNT(Policy_ID) AS Total_Policy,
    SUM(Premium_Amount) AS Total_Premium
FROM
    insurance_policies
GROUP BY State
ORDER BY Total_Policy DESC;

-- Compare the performance of different Sales_Channel in terms of policies sold and premium generated.
SELECT 
    Sales_channel,
    COUNT(Policy_ID) AS Total_Policy,
    SUM(Premium_Amount) AS Total_Premium
FROM
    insurance_policies
GROUP BY Sales_Channel
ORDER BY Total_Premium;

-- Also finding the data with respect the different financial year.
SELECT 
    Financial_Year,
    Sales_channel,
    COUNT(Policy_ID) AS Total_Policy,
    SUM(Premium_Amount) AS Total_Premium
FROM
    insurance_policies
GROUP BY Sales_Channel , Financial_Year
ORDER BY Total_Premium;

-- Identify which channels are most effective for specific policy types.
select Sales_Channel, Policy_Type from ( select Policy_Type, Sales_Channel, count(*) as Policy_count, 
ROW_NUMBER() over (Partition by Sales_Channel order by count(*) desc) as New from insurance_policies group by Policy_Type, Sales_Channel) 
as Ranked where New = 1;
  
 
-- Determine the claim rate basis of Gender, Sales channel, Financial year, Policy type, State (percentage of policies with claims)
-- Avg Claim rate
SELECT 
    ROUND(SUM(CASE
                WHEN Has_claimed = TRUE THEN 1
                ELSE 0
            END) * 100 / COUNT(Policy_ID),
            2) AS Claim_Rate_Avg
FROM
    insurance_policies;
 
 -- Avg Claim rate basis of Gender
 SELECT 
 Customer_Gender,
    ROUND(SUM(CASE
                WHEN Has_claimed = TRUE THEN 1
                ELSE 0
            END) * 100 / COUNT(Policy_ID),
            2) AS Claim_Rate_Avg
FROM
    insurance_policies
    group by Customer_Gender order by Customer_Gender desc;
 
  -- Avg Claim rate basis of Sales channel
  SELECT 
 Sales_Channel,
    ROUND(SUM(CASE
                WHEN Has_claimed = TRUE THEN 1
                ELSE 0
            END) * 100 / COUNT(Policy_ID),
            2) AS Claim_Rate_Avg
FROM
    insurance_policies
    group by Sales_Channel order by Sales_Channel desc;
 
 -- Avg Claim rate basis of Policy Type
SELECT 
 Policy_Type,
    ROUND(SUM(CASE
                WHEN Has_claimed = TRUE THEN 1
                ELSE 0
            END) * 100 / COUNT(Policy_ID),
            2) AS Claim_Rate_Avg
FROM
    insurance_policies
    group by Policy_Type order by Policy_Type desc;
    
 -- Avg Claim rate basis of Financial year
 SELECT 
 Financial_Year,
    ROUND(SUM(CASE
                WHEN Has_claimed = TRUE THEN 1
                ELSE 0
            END) * 100 / COUNT(Policy_ID),
            2) AS Claim_Rate_Avg
FROM
    insurance_policies
    group by Financial_Year order by Financial_Year desc;
    
 -- Avg Claim rate basis of States
 SELECT 
 State,
    ROUND(SUM(CASE
                WHEN Has_claimed = TRUE THEN 1
                ELSE 0
            END) * 100 / COUNT(Policy_ID),
            2) AS Claim_Rate_Avg
FROM
    insurance_policies
    group by State order by Claim_Rate_Avg desc;
    
-- Analyze the average Claim_Amount by Policy_Type and Customer_Age
-- Part 1
-- This will give the count of policies claimed in each Policy Type 
SELECT 
    Policy_Type,
    SUM(CASE
        WHEN Has_Claimed = TRUE THEN 1
        ELSE 0
    END) AS 'Count of Policy claimed'
FROM
    insurance_policies
GROUP BY Policy_Type
ORDER BY Policy_Type DESC;

-- This will give the count of policies not claimed in each Policy Type 
SELECT 
    Policy_Type,
    SUM(CASE
        WHEN Has_Claimed = FALSE THEN 1
        ELSE 1
    END) AS 'Count of Policy claimed'
FROM
    insurance_policies
GROUP BY Policy_Type
ORDER BY Policy_Type DESC;

-- Part 2
-- This give the total amount of policies claime in all the age groups also we will check for the policy count along with Premium
SELECT 
    CASE
        WHEN Customer_Age BETWEEN 18 AND 24 THEN '18-24'
        WHEN Customer_Age BETWEEN 25 AND 34 THEN '25-34'
        WHEN Customer_Age BETWEEN 35 AND 44 THEN '35-44'
        WHEN Customer_Age BETWEEN 45 AND 54 THEN '45-54'
        WHEN Customer_Age BETWEEN 55 AND 64 THEN '55-64'
		WHEN Customer_Age BETWEEN 65 AND 74 THEN '65-74'
        WHEN Customer_Age >= 75 THEN '70+'
        ELSE 'Unknown'
    END AS Age_Group,
    ROUND(AVG(Claim_Amount), 2) AS 'Avg Claim Amount',
    COUNT(Policy_ID) AS 'Total policy claimed'
FROM
    insurance_policies
WHERE
    Has_Claimed = TRUE
GROUP BY Age_Group
ORDER BY Age_Group;
    
-- This give the total amount of policies not claimed in all the age groups also we will check for the policy count along with Premium 
SELECT 
    CASE
        WHEN Customer_Age BETWEEN 18 AND 24 THEN '18-24'
        WHEN Customer_Age BETWEEN 25 AND 34 THEN '25-34'
        WHEN Customer_Age BETWEEN 35 AND 44 THEN '35-44'
        WHEN Customer_Age BETWEEN 45 AND 54 THEN '45-54'
        WHEN Customer_Age BETWEEN 55 AND 64 THEN '55-64'
		WHEN Customer_Age BETWEEN 65 AND 74 THEN '65-74'
        WHEN Customer_Age >= 75 THEN '70+'
        ELSE 'Unknown'
    END AS Age_Group,
    ROUND(AVG(Claim_Amount), 2) AS 'Avg Claim Amount',
    COUNT(Policy_ID) AS 'Total policy claimed'
FROM
    insurance_policies
WHERE
    Has_Claimed = false
GROUP BY Age_Group
ORDER BY Age_Group;
    
-- Explore if certain customer demographics are more prone to claims and the premium collected.
SELECT 
    State,
    SUM(CASE
        WHEN Has_Claimed = TRUE THEN 1
        ELSE 0
    END) AS 'Count of Policies Claimed',
    SUM(CASE
        WHEN Has_Claimed = FALSE THEN 1
        ELSE 0
    END) AS 'Count of Policies Not Claimed',
    ROUND(SUM(DISTINCT CASE
                WHEN Has_Claimed = TRUE THEN 1
                ELSE 0
            END) * 100 / COUNT(Policy_ID),
            2) AS 'Claim rate',
    SUM(Premium_Amount) AS 'Total premium collected'
FROM
    insurance_policies
GROUP BY State
ORDER BY 'Claim rate' DESC;
    
-- Top 10 states with high claim ratio thus these can be said to be a risky state
 SELECT 
 State,
    ROUND(SUM(CASE
                WHEN Has_claimed = TRUE THEN 1
                ELSE 0
            END) * 100 / COUNT(Policy_ID),
            2) AS Claim_Rate_Avg
FROM
    insurance_policies
    group by State order by Claim_Rate_Avg desc limit 10;

-- Top 10 states with low claim ratio thus these can be said to be a profitable state
 SELECT 
 State,
    ROUND(SUM(CASE
                WHEN Has_claimed = TRUE THEN 1
                ELSE 0
            END) * 100 / COUNT(Policy_ID),
            2) AS Claim_Rate_Avg
FROM
    insurance_policies
    group by State order by Claim_Rate_Avg limit 10;


-- Analyse the data on the basis of Months and Quarter.
-- Quarters of FY 2022-23
SELECT 
    SUM(Premium_Amount) AS 'Total sales',
    CONCAT('Q', QUARTER(Sale_Date)) AS 'Quarters',
    Financial_Year
FROM
    insurance_policies
    where Financial_Year = 'FY2022-23'
GROUP BY Quarters , Financial_Year
ORDER BY Financial_Year ASC , Quarters ASC;

-- Quarter of FY 2023-24
SELECT 
    SUM(Premium_Amount) AS 'Total sales',
    CONCAT('Q', QUARTER(Sale_Date)) AS 'Quarters',
    Financial_Year
FROM
    insurance_policies
    where Financial_Year = 'FY2023-24'
GROUP BY Quarters , Financial_Year
ORDER BY Financial_Year ASC , Quarters ASC;

-- Quarter of FY 2024-25
SELECT 
    SUM(Premium_Amount) AS 'Total sales',
    CONCAT('Q', QUARTER(Sale_Date)) AS 'Quarters',
    Financial_Year
FROM
    insurance_policies
    where Financial_Year = 'FY2024-25'
GROUP BY Quarters , Financial_Year
ORDER BY Financial_Year ASC , Quarters ASC;

-- Monthly of FY 2022-23
SELECT 
    SUM(Premium_Amount) AS 'Total sales',
    Month(Sale_Date) AS 'Months',
    monthname(Sale_Date) AS 'Months_Name',
    Financial_Year
FROM
    insurance_policies
    where Financial_Year = 'FY2022-23'
GROUP BY Months , Financial_Year, Months_Name
ORDER BY Financial_Year ASC , Months ASC;

-- Monthly of FY 2023-24
SELECT 
    SUM(Premium_Amount) AS 'Total sales',
    Month(Sale_Date) AS 'Months',
    monthname(Sale_Date) AS 'Months_Name',
    Financial_Year
FROM
    insurance_policies
    where Financial_Year = 'FY2023-24'
GROUP BY Months , Financial_Year, Months_Name
ORDER BY Financial_Year ASC , Months ASC;

-- Monthly of FY 2024-25   
SELECT 
    SUM(Premium_Amount) AS 'Total sales',
    Month(Sale_Date) AS 'Months',
    monthname(Sale_Date) AS 'Months_Name',
    Financial_Year
FROM
    insurance_policies
    where Financial_Year = 'FY2024-25'
GROUP BY Months , Financial_Year, Months_Name
ORDER BY Financial_Year ASC , Months ASC;   

-- Calculating monthly claim %age and the profit %age of all the FY 
-- FY 2022-23
SELECT 
    SUM(Premium_Amount) AS 'Total_sales',
    SUM(Claim_Amount) as 'Total_claim',
    ROUND((SUM(Claim_Amount)/SUM(Premium_Amount))*100,2) as 'Claim_%age',
    ROUND((SUM(Premium_Amount) - SUM(Claim_Amount)) / SUM(Premium_Amount) * 100, 2) as 'Profit_%age',
    MONTHNAME(Sale_Date) AS 'Months_Name',
    Financial_Year
FROM
    insurance_policies
    where Financial_Year = 'FY2022-23'
GROUP BY Financial_Year, Months_Name
ORDER BY Financial_Year ASC , Months_Name ASC;   

-- FY 2023-24
SELECT 
    SUM(Premium_Amount) AS 'Total_sales',
    SUM(Claim_Amount) as 'Total_claim',
    ROUND((SUM(Claim_Amount)/SUM(Premium_Amount))*100,2) as 'Claim_%age',
    ROUND((SUM(Premium_Amount) - SUM(Claim_Amount)) / SUM(Premium_Amount) * 100, 2) as 'Profit_%age',
    MONTHNAME(Sale_Date) AS 'Months_Name',
    Financial_Year
FROM
    insurance_policies
    where Financial_Year = 'FY2023-24'
GROUP BY Financial_Year, Months_Name
ORDER BY Financial_Year ASC , Months_Name ASC;   
    
-- FY 2024-25
SELECT 
    SUM(Premium_Amount) AS 'Total_sales',
    SUM(Claim_Amount) as 'Total_claim',
    ROUND((SUM(Claim_Amount)/SUM(Premium_Amount))*100,2) as 'Claim_%age',
    ROUND((SUM(Premium_Amount) - SUM(Claim_Amount)) / SUM(Premium_Amount) * 100, 2) as 'Profit_%age',
    MONTHNAME(Sale_Date) AS 'Months_Name',
    Financial_Year
FROM
    insurance_policies
    where Financial_Year = 'FY2024-25'
GROUP BY Financial_Year, Months_Name
ORDER BY Financial_Year ASC , Months_Name ASC;

-- Calculating Quarterly claim %age and the profit %age of all the FY
-- Quarters of FY 2022-23
SELECT 
    SUM(Premium_Amount) AS 'Total sales',
    CONCAT('Q', QUARTER(Sale_Date)) AS 'Quarters',
    ROUND((SUM(Claim_Amount)/SUM(Premium_Amount))*100,2) as 'Claim_%age',
    ROUND((SUM(Premium_Amount) - SUM(Claim_Amount)) / SUM(Premium_Amount) * 100, 2) as 'Profit_%age',
    Financial_Year
FROM
    insurance_policies
    where Financial_Year = 'FY2022-23'
GROUP BY Quarters , Financial_Year
ORDER BY Financial_Year ASC , Quarters ASC;

-- Quarter of FY 2023-24
SELECT 
    SUM(Premium_Amount) AS 'Total sales',
    CONCAT('Q', QUARTER(Sale_Date)) AS 'Quarters',
    ROUND((SUM(Claim_Amount)/SUM(Premium_Amount))*100,2) as 'Claim_%age',
    ROUND((SUM(Premium_Amount) - SUM(Claim_Amount)) / SUM(Premium_Amount) * 100, 2) as 'Profit_%age',
    Financial_Year
FROM
    insurance_policies
    where Financial_Year = 'FY2023-24'
GROUP BY Quarters , Financial_Year
ORDER BY Financial_Year ASC , Quarters ASC;

-- Quarter of FY 2024-25
SELECT 
    SUM(Premium_Amount) AS 'Total sales',
    CONCAT('Q', QUARTER(Sale_Date)) AS 'Quarters',
    ROUND((SUM(Claim_Amount)/SUM(Premium_Amount))*100,2) as 'Claim_%age',
    ROUND((SUM(Premium_Amount) - SUM(Claim_Amount)) / SUM(Premium_Amount) * 100, 2) as 'Profit_%age',
    Financial_Year
FROM
    insurance_policies
    where Financial_Year = 'FY2024-25'
GROUP BY Quarters , Financial_Year
ORDER BY Financial_Year ASC , Quarters ASC;
    
-- Total claim %age and the profit %age of all the Financila years.
SELECT 
    SUM(Premium_Amount) AS 'Total sales',
    SUM(Claim_Amount) AS 'Total Claim',
    ROUND((SUM(Claim_Amount)/SUM(Premium_Amount))*100,2) as 'Claim_%age',
    ROUND((SUM(Premium_Amount) - SUM(Claim_Amount)) / SUM(Premium_Amount) * 100, 2) as 'Profit_%age',
    Financial_Year
FROM
    insurance_policies
GROUP BY Financial_Year
ORDER BY Financial_Year;



    
    
    
    
    
    
    
    


