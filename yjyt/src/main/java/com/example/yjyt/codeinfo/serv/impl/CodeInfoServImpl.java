package com.example.yjyt.codeinfo.serv.impl;

import com.alibaba.fastjson.JSONArray;
import com.alibaba.fastjson.JSONObject;
import com.baomidou.mybatisplus.extension.service.impl.ServiceImpl;
import com.example.yjyt.codeinfo.dao.CodeInfoDao;
import com.example.yjyt.codeinfo.domain.CodeInfo;
import com.example.yjyt.codeinfo.domain.dto.CodeDTO;
import com.example.yjyt.codeinfo.domain.vo.CodeInfoVO;
import com.example.yjyt.codeinfo.domain.vo.Segment;
import com.example.yjyt.codeinfo.serv.CodeInfoServ;
import org.springframework.beans.BeanUtils;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.text.SimpleDateFormat;
import java.util.*;

@Service
public class CodeInfoServImpl extends ServiceImpl<CodeInfoDao, CodeInfo> implements CodeInfoServ {
    @Autowired
    private CodeInfoDao codeInfoDao;

    final static String ERROR_TYPE = "[ERROR_TYPE]";

    final static List<String> CODE_NAMES = new ArrayList<>(Arrays.asList("产品实例编码", "用户编码"));
    final static List<String> CODE_TYPES = new ArrayList<>(Arrays.asList("UmppModu", "User"));

    @Override
    public JSONObject previewExpression(List<Segment> segments) {
        StringBuilder sb = new StringBuilder();
        segments.stream().filter(seg -> seg.getValue() != null && seg.getValue().length() > 0).forEach(item -> {
            String expression = segmentToExpression(item);
            if (!ERROR_TYPE.equals(expression)) {
                sb.append('$').append(expression);
            }
        });
        String expression = sb.substring(1);    // ??? 为啥？ 开头的$符号要去掉吗？
        JSONObject obj = new JSONObject();
        obj.put("expression", expression);  // expression 表达式
        obj.put("previewText", genCode(expression, 1));     // 生成一个编码实例，实例而已，并不是直接使用了的
        return obj;
    }

    private String segmentToExpression(Segment seg) {
        Integer type = seg.getType();
        switch (type) {
            //字符串常量
            case 1:
                return '%' + seg.getValue();
            //流水号
            case 2:
                return "flow" + seg.getValue().charAt(0);
            //日期格式化
            case 3:
                return seg.getValue();
            //用户自定义
            case 4:
                return "user";
            default:
        }
        return ERROR_TYPE;
    }

    private String genFlowNum(int length, int flowNum) {
        String fmt = String.format("%%0%dd", length);
        return String.format(fmt, flowNum);
    }

    private String genTimeStamp(String value) {
        switch (value) {
            case "st": {
                // 简易时间戳
                SimpleDateFormat sdf = new SimpleDateFormat("yyyyMMdd");
                return sdf.format(new Date());
            }
            case "ct": {
                // 复杂时间戳
                SimpleDateFormat sdf = new SimpleDateFormat("yyyyMMddHHmmss");
                return sdf.format(new Date());
            }
            case "yt": {
                // 只有年份的时间戳
                SimpleDateFormat sdf = new SimpleDateFormat("yyyy");
                return sdf.format(new Date());
            }
            default:
        }
        return "";
    }


    @Override
    public CodeInfo findById(String id) {
        CodeInfo info = codeInfoDao.findById(id);
        info.setPreviewText(genCode(info.getExpression(), 1));
        return toView(info);
    }

    @Override
    public void add(CodeInfo codeInfo) {
        CodeInfo info = codeInfoDao.findByCodeName(codeInfo.getName());
        if (info != null) {
            throw new RuntimeException("名称已存在");
        }
        codeInfo.setSeq(codeInfoDao.getMaxSeq());
        codeInfo.setFlowNum(1);
        codeInfo.setStatus(0);
        save(codeInfo);
    }

    @Override
    public void update(CodeDTO dto) {
        codeInfoDao.update(dto);
    }

    @Override
    @Transactional
    public void start(String id) {
        codeInfoDao.startById(id);
    }

    @Override
    public void stopById(String id) {
        codeInfoDao.stopById(id);
    }

    private CodeInfoVO toView(CodeInfo code) {
        CodeInfoVO vo = new CodeInfoVO();
        String expression = code.getExpression();
        List<Segment> segments = toSegs(expression, code.getFlowNum());
        BeanUtils.copyProperties(code, vo);
        vo.setSegs(segments);
        return vo;
    }

    private List<Segment> toSegs(String expression, Integer flowNum) {
        String[] segs = expression.split("\\$");
        List<Segment> segments = new ArrayList<>(segs.length);
        int type = 0;
        String str = "";
        for (int i = 0; i < segs.length; i++) {
            String s = segs[i];
            if ("%".equals(s.substring(0, 1))) {
                // 开头是% 后面接普通字符串
                str = s.substring(1);
                type = 1;
            } else if (s.length() > 3) {
                if ("flow".equals(s.substring(0, 4))) {
                    str = s.substring(4, 5);
                    type = 2;
                } else if ("user".equals(s)) {
                    str = s;
                    type = 4;
                }
            } else if (s.length() > 1) {
                type = 3;
                str = s.substring(0, 2);
            }


            segments.add(new Segment(str, type, i));
        }
        return segments;
    }

    @Override
    public String genCode(String expression, Integer flowNum) {
        StringBuilder code = new StringBuilder();
        // $ 为分隔符 不能转义，将规则分开
        try {
            String[] a = expression.split("\\$");
            for (String s : a) {
                if ("%".equals(s.substring(0, 1))) {
                    // 开头是% 后面接普通字符串
                    String str = s.substring(1);
                    code.append(str);
                } else if (s.length() > 3) {
                    if ("flow".equals(s.substring(0, 4))) {
                        String r = s.substring(4, 5);
                        int l = Integer.parseInt(r);
                        int count = flowNum == null ? 0 : flowNum;
                        code.append(genFlowNum(l, count));

                    } else if ("rand".equals(s.substring(0, 4))) {
                        String r = s.substring(4, 5);
                        Random ra = new Random();
                        int l = Integer.parseInt(r);
                        int limit = 1;
                        for (int i = 0; i < l - 1; i++) {
                            limit *= 10;
                        }
                        code.append(genFlowNum(l, ra.nextInt(limit)));
                    } else if ("user".equals(s)) {
                        code.append("【】");
                    }
                } else if (s.length() > 1) {
                    String type = s.substring(0, 2);
                    code.append(genTimeStamp(type));
                }
            }
            if ("".equals(code.toString())) {
                return null;
            }
            return code.toString();
        } catch (Exception e) {
            e.printStackTrace();
            return null;
        }
    }

    @Override
    public void deleteById(String id) {
        CodeInfo code = findById(id);
        if (1 == code.getStatus()) {
            throw new RuntimeException("使用中的编码不可删除");
        }
        codeInfoDao.deleteById(id);
    }

    @Override
    @Transactional
    public String getCode(String className) {
        CodeInfo code = codeInfoDao.findByClassName(className);
        if (code == null) return "";
        String str = genCode(code.getExpression(), code.getFlowNum());
        codeInfoDao.nextFlow(code);
        return str;
    }

    @Override
    public JSONArray getCurrentOptions() {
        JSONArray arr = new JSONArray();
        for (int i = 0; i < CODE_NAMES.size(); i++) {
            JSONObject obj = new JSONObject();
            obj.put("label", CODE_NAMES.get(i));
            obj.put("type", CODE_TYPES.get(i));
            arr.add(obj);
        }
        return arr;
    }


    // 同一个 className 可能有多个编码器。
    // 同一个 className 下的多个编码器，只能有一个生效。
    @Override
    @Transactional(rollbackFor = Exception.class)
    public void enable(String id) {
        CodeInfo info = codeInfoDao.findById(id);
        CodeInfo curInfo = codeInfoDao.findByClassName(info.getClassName());
        if (curInfo != null) {
            disable(curInfo.getId());
        }
        codeInfoDao.enable(id);
    }

    @Override
    public void disable(String id) {
        codeInfoDao.disable(id);
    }

    @Override
    public JSONArray getIdNames() {
        List<CodeInfo> list = codeInfoDao.list();
        JSONArray arr = new JSONArray();
        list.forEach(item -> {
            JSONObject obj = new JSONObject();
            obj.put("id", item.getId());
            obj.put("name", item.getName());
            arr.add(obj);
        });
        return arr;
    }

    @Override
    public List<Segment> getInputBox(String id) {
        CodeInfo codeInfo = findById(id);

        return getCodeSegs(codeInfo.getExpression(), codeInfo.getFlowNum());
    }

    @Override
    public String getFinalCode(String id, List<Segment> segs) {
        JSONObject obj = new JSONObject();
        obj.put("id", id);
        // s.getType() == 2 表示流水号
        long count = segs.stream().filter(s -> s.getType() == 2).count();
        List<Integer> flows = getFlows(id, count);
        int i = 0;
        for (Segment s : segs) {//如果是流水号要从数据库里面获取
            if (s.getType() == 2) {
                s.setValue(String.valueOf(flows.get(i)));
                i++;
            }
        }
        obj.put("segs", segs);
        return obj.toJSONString();
    }

    /**
     * 获取一定数量的流水号
     *
     * @param id    当前编码id
     * @param count 需要的流水号数量
     * @return 大小为count的连续流水号数组
     */
    private List<Integer> getFlows(String id, long count) {
        List<Integer> flows = new LinkedList<>();
        if (count == 0) return flows;
        CodeInfo code = codeInfoDao.findById(id);
        Integer flow = code.getFlowNum();
        for (int i = 0; i < count; i++) {
            flows.add(flow + i);
        }
        codeInfoDao.updateFlow(id, flow, count);
        return flows;
    }

    private List<Segment> getCodeSegs(String expression, Integer flowNum) {
        List<Segment> segs = new LinkedList<>();
        // $ 为分隔符 不能转义，将规则分开
        try {
            String[] a = expression.split("\\$");
            int i = 0;
            for (String s : a) {
                String str = "";
                int type = 0;
                if ("%".equals(s.substring(0, 1))) {
                    // 开头是% 后面接普通字符串
                    str = s.substring(1);
                    type = 1;
                } else if (s.length() > 3) {
                    if ("flow".equals(s.substring(0, 4))) {
                        String r = s.substring(4, 5);
                        int l = Integer.parseInt(r);
                        int count = flowNum == null ? 0 : flowNum;
                        str = genFlowNum(l, count);
                        type = 2;
                    } else if ("user".equals(s)) {
                        type = 4;
                        str = "";
                    }
                } else if (s.length() > 1) {
                    String t = s.substring(0, 2);
                    str = genTimeStamp(t);
                    type = 3;
                }

                segs.add(new Segment(str, type, 0));
            }
            return segs;
        } catch (Exception e) {
            e.printStackTrace();
            return null;
        }
    }
}
