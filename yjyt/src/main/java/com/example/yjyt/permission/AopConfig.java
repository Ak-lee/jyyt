package com.example.yjyt.permission;

import org.aspectj.lang.JoinPoint;
import org.aspectj.lang.annotation.Aspect;
import org.aspectj.lang.annotation.Before;
import org.aspectj.lang.annotation.Pointcut;
import org.aspectj.lang.reflect.MethodSignature;
import org.springframework.core.DefaultParameterNameDiscoverer;
import org.springframework.core.ParameterNameDiscoverer;
import org.springframework.stereotype.Component;
import org.springframework.web.context.request.RequestAttributes;
import org.springframework.web.context.request.RequestContextHolder;
import org.springframework.web.context.request.ServletRequestAttributes;

import javax.servlet.http.HttpServletRequest;
import java.lang.reflect.Method;
import java.util.HashMap;
import java.util.Set;

@Aspect
@Component
public class AopConfig {

    @Pointcut("@annotation(com.example.yjyt.permission.HasRole)")
    public void pointcut() {
    }

    @Before("pointcut()")
    // 前置通知
    public void before(JoinPoint joinPoint) throws ClassNotFoundException, NoSuchMethodException {
        System.out.println("before---------------");

        // 尝试获取参数运行时的调用值， 特别是传入的 lineId.
        // classType 是某个 controller
        String classType = joinPoint.getTarget().getClass().getName();
        // 获取方法名
        String methodName = joinPoint.getSignature().getName();

        // 参数值
        Object[] args = joinPoint.getArgs();
        Class<?>[] classes = new Class[args.length];
        for (int k = 0; k < args.length; k++) {
            classes[k] = args[k].getClass();
        }
        ParameterNameDiscoverer pnd = new DefaultParameterNameDiscoverer();
        // 获取指定的方法，第二个参数可以不穿，但是为了防止有重载的现象，还是需要传入参数的类型
        Method method = Class.forName(classType).getMethod(methodName, classes);

        // 参数名
        String[] parameterNames = pnd.getParameterNames(method);
        // 通过 map 封装参数和参数值
        HashMap<String, Object> paraMap = new HashMap<>();
        for (int i = 0; i < parameterNames.length; i++) {
            paraMap.put(parameterNames[i], args[i]);
        }

        String s = paraMap.toString();
        System.out.println("+++++++++++++++++++++++++++++");
        System.out.println(s);
        System.out.println("+++++++++++++++++++++++++++++++++++++++++++++++++");
//
//        // 获取到 HttpServletRequest， ThreadLocal
//        RequestAttributes requestAttributes = RequestContextHolder.getRequestAttributes();
//        ServletRequestAttributes servletRequestAttributes = (ServletRequestAttributes) requestAttributes;
//        HttpServletRequest request = servletRequestAttributes.getRequest();
//
//        String username = request.getParameter("username");
//
//        // 获取当前用户的角色集合
//        Set<String> userRoles = CacheManager.USER_ROLE_MAP.get(username);
//
//        // 获取当前请求的方法上的注解 hasRole 中设置的角色
//        MethodSignature signature = (MethodSignature) joinPoint.getSignature();
//
//        // 反射获取当前被调用的方法
//        Method method = signature.getMethod();
//
//        // 判断当前方法是否有 hasRole 注解
//        // 如果有，判断是否用户注解属性中要求的角色
//        // 如果没有 hasRole 注解，那么说明方法不需要用户的角色，可以匿名访问
//        HasRole hasRole = method.getDeclaredAnnotation(HasRole.class);
//        if (hasRole != null && (userRoles == null || !userRoles.contains(hasRole.value()))) {
//            throw new RuntimeException("用户没有访问权限");
//        }
    }
}
