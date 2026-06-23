data custstep.cs_dqmcparsed;
    length locale definition token $50;
    infile cards dlm="," ;
    input locale $ definition token $;
    cards;
English - United Kingdom,City - State/Province - Postal Code,District/Village
English - United Kingdom,City - State/Province - Postal Code,Town/City
English - United Kingdom,City - State/Province - Postal Code,County
English - United Kingdom,City - State/Province - Postal Code,Country
English - United Kingdom,City - State/Province - Postal Code,Postcode
English - United Kingdom,City - State/Province - Postal Code,Additional Info
English - United Kingdom,Name,Prefix
English - United Kingdom,Name,Given Name
English - United Kingdom,Name,Middle Name
English - United Kingdom,Name,Family Name
English - United Kingdom,Name,Suffix
English - United Kingdom,Name,Title/Additional Info
English - United States,City - State/Province - Postal Code,City
English - United States,City - State/Province - Postal Code,State
English - United States,City - State/Province - Postal Code,ZIP
English - United States,Name,Prefix
English - United States,Name,Given Name
English - United States,Name,Middle Name
English - United States,Name,Family Name
English - United States,Name,Suffix
English - United States,Name,Title/Additional Info
English - Canada,Name,Prefix
English - Canada,Name,Given Name
English - Canada,Name,Middle Name
English - Canada,Name,Family Name
English - Canada,Name,Suffix
English - Canada,Name,Title/Additional Info
French - Canada,Name,Prefix
French - Canada,Name,Given Name
French - Canada,Name,Middle Name
French - Canada,Name,Family Name
French - Canada,Name,Suffix
French - Canada,Name,Title/Additional Info
French - France,City - State/Province - Postal Code,Geographical City
French - France,City - State/Province - Postal Code,Postal Code
French - France,City - State/Province - Postal Code,City
French - France,City - State/Province - Postal Code,Cedex
French - France,City - State/Province - Postal Code,Cedex Number
French - France,City - State/Province - Postal Code,Special Distribution
French - France,City - State/Province - Postal Code,Special Distribution Number
French - France,City - State/Province - Postal Code,Department
French - France,City - State/Province - Postal Code,Administrative District
French - France,Name,Prefix
French - France,Name,Given Name
French - France,Name,Middle Name
French - France,Name,Family Name
French - France,Name,Suffix
French - France,Name,Title/Additional Info
French - France,Organization,Name
French - France,Organization,Legal Form
French - France,Organization,Site
French - France,Organization,Additional Info
German - Germany,Name,Prefix
German - Germany,Name,Given Name
German - Germany,Name,Middle Name
German - Germany,Name,Family Name
German - Germany,Name,Suffix
German - Germany,Name,Title/Additional Info
Italian - Italy,Name,Prefix
Italian - Italy,Name,Given Name
Italian - Italy,Name,Family Name
Italian - Italy,Name,Suffix
Italian - Italy,Name,Title/Additional Info
Italian - Italy,Address,Street Type
Italian - Italy,Address,Additional Street Type
Italian - Italy,Address,Street Name
Italian - Italy,Address,Street Number
Italian - Italy,Address,Street Number Extension
Italian - Italy,Address,Building Name
Italian - Italy,Address,PO Box
Italian - Italy,Address,Additional Info
Italian - Italy,Address,Post Office Location
Italian - Italy,City - State/Province - Postal Code,City
Italian - Italy,City - State/Province - Postal Code,State/Province
Italian - Italy,City - State/Province - Postal Code,Postal Code
Italian - Italy,City - State/Province - Postal Code,Additional Info
Italian - Italy,Organization,Name
Italian - Italy,Organization,Legal Form
Italian - Italy,Organization,Additional Info
Italian - Italy,Organization,Site
Spanish - Spain,Name,Prefix
Spanish - Spain,Name,Given Name
Spanish - Spain,Name,Family Name 1
Spanish - Spain,Name,Family Name 2
Spanish - Spain,Name,Suffix
Spanish - Spain,Name,Title/Additional Info
Spanish - Spain,City - State/Province - Postal Code,Postal Code
Spanish - Spain,City - State/Province - Postal Code,City
Spanish - Spain,City - State/Province - Postal Code,Province
;
