
-- 获取某个package下面模型的分析权限
select object_name, SUBSTRING_REGEXPR('applyPrivilegeType="(.*?)"' in cdata group 1) 
  from "_SYS_REPO"."ACTIVE_OBJECT"
 where PACKAGE_ID = 'AVIC' -- package fully name