options mstored sasmstore=macros;
libname macros '/var/sas_projects/latvia/belfius/macros';
%DCM_LOAD_CUSTOM_FUNCTION(FunctionDir='/Public/Custom Functions/Nested DataGrids',
                          FunctionFile='nested_dataGrid_addCharacterColumn.cf');
