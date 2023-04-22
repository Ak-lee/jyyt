package com.example.yjyt.domain;

import java.util.Date;

public class predResult {
    private String trainId;
    private  Integer mileage;
    private Date calendar;
    private Date date;//训练数据终止时间
    public predResult() {
    }

    public predResult(String trainId, Date calendar) {
        this.trainId = trainId;
        this.calendar = calendar;
    }

    public Date getDate() {
        return date;
    }

    public void setDate(Date date) {
        this.date = date;
    }

    public String getTrainId() {
        return trainId;
    }

    public void setTrainId(String trainId) {
        this.trainId = trainId;
    }

    public Integer getMileage() {
        return mileage;
    }

    public void setMileage(Integer mileage) {
        this.mileage = mileage;
    }

    public Date getCalendar() {
        return calendar;
    }

    public void setCalendar(Date calendar) {
        this.calendar = calendar;
    }

    @Override
    public String toString() {
        return "predResult{" +
                "train_id='" + trainId + '\'' +
                ", mileage=" + mileage +
                ", calendar=" + calendar +
                '}';
    }
}
