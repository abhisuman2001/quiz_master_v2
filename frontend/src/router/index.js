import { createRouter, createWebHistory } from 'vue-router'
import { jwtDecode } from 'jwt-decode';
import HomePage from '../views/HomePage.vue'
import AdminLayout from '../layouts/AdminLayout.vue'

const routes = [
  { path: '/', name: 'HomePage', component: HomePage },
  { path: '/login', name: 'Login', component: () => import('../views/Login.vue') },
  { path: '/register', name: 'Register', component: () => import('../views/Register.vue') },
  {
    path: '/admin',
    component: AdminLayout,
    meta: { requiresAuth: true, role: 'admin' },
    children: [
      { path: 'dashboard', name: 'AdminDashboard', component: () => import('../views/AdminDashboard.vue') },
      { path: 'subjects', name: 'SubjectManagement', component: () => import('../views/admin/SubjectManagement.vue') },
      { path: 'chapters', name: 'ChapterManagement', component: () => import('../views/admin/ChapterManagement.vue') },
      { path: 'quizzes', name: 'QuizManagement', component: () => import('../views/admin/QuizManagement.vue') },
      {
        path: 'quizzes/:quiz_id/questions',
        name: 'QuestionManagement',
        component: () => import('../views/admin/QuestionManagement.vue'),
        props: true
      }
    ]
  },
  { path: '/dashboard', name: 'UserDashboard', component: () => import('../views/UserDashboard.vue'), meta: { requiresAuth: true, role: 'user' } }
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes
})

router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('accessToken');
  if (to.meta.requiresAuth) {
    if (token) {
      try {
        const userData = jwtDecode(token);
        const userRole = userData.role;
        if (to.meta.role && to.meta.role === userRole) {
          next();
        } else {
          next(userRole === 'admin' ? '/admin/dashboard' : '/dashboard');
        }
      } catch (e) {
        localStorage.removeItem('accessToken');
        next('/login');
      }
    } else {
      next('/login');
    }
  } else {
    next();
  }
});

export default router