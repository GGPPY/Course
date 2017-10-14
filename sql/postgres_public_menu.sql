INSERT INTO public.menu (id, parent, name, sort, route) VALUES (2, 0, '报名管理', 1, null);
INSERT INTO public.menu (id, parent, name, sort, route) VALUES (1, 0, '设置', 99, null);
INSERT INTO public.menu (id, parent, name, sort, route) VALUES (6, 1, '用户管理', 1, null);
INSERT INTO public.menu (id, parent, name, sort, route) VALUES (7, 1, '用户组管理', 2, null);
INSERT INTO public.menu (id, parent, name, sort, route) VALUES (8, 1, '修改密码', 3, null);
INSERT INTO public.menu (id, parent, name, sort, route) VALUES (5, 2, '科目管理', 1, null);
INSERT INTO public.menu (id, parent, name, sort, route) VALUES (3, 2, '课程发布', 2, '/course_manage');
INSERT INTO public.menu (id, parent, name, sort, route) VALUES (4, 2, '学员管理', 3, '/signed');