#include <math.h>
#include <iostream>
#include <iomanip>
#include <list>


#include "Include/TXNMath.h"
using namespace std;

const double g_dEPS = .0000001;

namespace TXN_NS_MATH
{
	//计算p1p2和p1p3的叉积
	double Direction(const TXNPoint& p1,const TXNPoint& p2,const TXNPoint& p3)
	{
		TXNPoint d1=make_pair(p3.first-p1.first,p3.second-p1.second);
		TXNPoint d2=make_pair(p2.first-p1.first,p2.second-p1.second);
		return d1.first*d2.second-d1.second*d2.first;
	}

	//确认p3在p1p2上，还是在p1p2的延长线上
	bool OnSegment(const TXNPoint& p1,const TXNPoint& p2,const TXNPoint& p3){
		double x_min,x_max,y_min,y_max;
		if(p1.first<p2.first){
			x_min=p1.first;
			x_max=p2.first;
		}else{
			x_min=p2.first;
			x_max=p1.first;
		}
		if(p1.second<p2.second){
			y_min=p1.second;
			y_max=p2.second;
		}else{
			y_min=p2.second;
			y_max=p1.second;
		}
		if(p3.first<x_min || p3.first>x_max || p3.second<y_min || p3.second>y_max)
			return false;
		else
			return true;
	}


	//判断线段是否相交
	bool SegmentIntersect(const TXNPoint& p1,const TXNPoint& p2,const TXNPoint& p3,const TXNPoint& p4){
		double d1=Direction(p3,p4,p1);
		double d2=Direction(p3,p4,p2);
		double d3=Direction(p1,p2,p3);
		double d4=Direction(p1,p2,p4);

		if(d1*d2<0 && d3*d4<0)
			return true;
		else if(d1==0 && OnSegment(p3,p4,p1))
			return true;
		else if(d2==0 && OnSegment(p3,p4,p2))
			return true;
		else if(d3==0 && OnSegment(p1,p2,p3))
			return true;
		else if(d4==0 && OnSegment(p1,p2,p4))
			return true;
		else
			return false;
	}


	//获取线段长度
	double GetLineLength(const TXNPoint& p1,const TXNPoint& p2)
	{
		return sqrt(((p1.first-p2.first)*(p1.first-p2.first)+(p1.second-p2.second)*(p1.second-p2.second)));		
	}


	//获取三角形面积 （x1y2+x2y3+x3y1-x1y3-x2y1-x3y2）/2
	double GetTriangleArea(const TXNPoint& p1,const TXNPoint& p2,const TXNPoint& p3)
	{
        return fabs(p1.first*p2.second+p2.first*p3.second+p3.first*p1.second-
			p1.first*p3.second-p2.first*p1.second-p3.first*p2.second)/2;
	}



	//获取点到直线距离 p3到直线p1p2距离
	double GetVerticalLineLength(const TXNPoint& p1,const TXNPoint& p2,const TXNPoint& p3)
	{
		double dd = GetTriangleArea(p1,p2,p3);
		double zz= GetLineLength(p1,p2);
		return 2*GetTriangleArea(p1,p2,p3)/GetLineLength(p1,p2);
	}

	//获取两点式参数A（Ax+By+C=0）
	double GetLineParaA(const TXNPoint& p1,const TXNPoint& p2)
	{
		return p1.second-p2.second;
	}



	//获取两点式参数B（Ax+By+C=0）
	double GetLineParaB(const TXNPoint& p1,const TXNPoint& p2)
	{
		return p2.first-p1.first;
	}



	//获取两点式参数C（Ax+By+C=0）
	double GetLineParaC(const TXNPoint& p1,const TXNPoint& p2)
	{
		return (p2.second-p1.second)*p2.first+(p1.first-p2.first)*p2.second;
	}

    //获取直线p1、p2距离dDis的直线一般式Ax+By+C=0 的C值，一般有两个(其中A=y1-y2；B=x2-x1),这里取三角形内的平行线
    /*               p3
                    /\
                   /  \
                --/----\--
                 / dDis \
              p1/--------\p2
     */
	double GetLineParaC(const TXNPoint& p1,const TXNPoint& p2, const TXNPoint& p3, double dDis)
	{
		double dC = GetLineParaC(p1,p2);
		double dTmp = GetLineLength(p1,p2)*dDis;

		double dA = GetLineParaA(p1,p2);
		double dB = GetLineParaB(p1,p2);
		double dValue = dA*p3.first+dB*p3.second+dC;

		if (dValue > 0)
		{
			return dC-dTmp;
		}

		return dC+dTmp;
	}




	//两直线交点（一般式）
	TXNPoint GetIntersectPoint(const double dAP, const double dBP, const double dCP, const double dAL, const double dBL, const double dCL)
	{
		return make_pair(
			(dBP*dCL-dBL*dCP)/(dBL*dAP-dBP*dAL),
			(dAP*dCL-dAL*dCP)/(dAL*dBP-dAP*dBL)
			);
	}

    //根据4点及收缩距离dDis 输出收缩点列
    TXNPointArr GetShrinkResults(const TXNPointArr& ptArr,double dDis)
    {
        TXNPointArr arrValue;
        if (SegmentIntersect(ptArr[0],ptArr[1],ptArr[2],ptArr[3]))
        {
            return arrValue;
        }

        for(int i = 0; i < ptArr.size(); i++){
            int j = i+1;
            if(i+1 == ptArr.size()){
                j = 0;
            }
            int k = j+1;

            double dA1 = GetLineParaA(ptArr[i],ptArr[j]);
            double dB1 = GetLineParaB(ptArr[i],ptArr[j]);
            double dC1 = GetLineParaC(ptArr[i],ptArr[j], ptArr[k],dDis);

            double dA2 = GetLineParaA(ptArr[k],ptArr[j]);
            double dB2 = GetLineParaB(ptArr[k],ptArr[j]);
            double dC2 = GetLineParaC(ptArr[k],ptArr[j], ptArr[i],dDis);

            TXNPoint ptIntersect = GetIntersectPoint(dA1, dB1, dC1, dA2, dB2, dC2);

            arrValue.push_back(ptIntersect);
        }

        //调整次序
        TXNPoint ptLast = *arrValue.rbegin();
        arrValue.pop_back();
        arrValue.insert(arrValue.begin(), ptLast);

        return arrValue;
    }



	//根据4点及航路距离dDis 输出航路规划点列
	TXNPointArr GetResults(const TXNPoint& p1,const TXNPoint& p2,const TXNPoint& p3,const TXNPoint& p4,double dDis)
	{
		TXNPointArr arrValue;
		if (SegmentIntersect(p1,p2,p3,p4))
		{
			return arrValue;
		}

		//比较点p3、p4到直线p1、p2的距离
		double dLen3 = GetVerticalLineLength(p1,p2,p3);
		double dLen4 = GetVerticalLineLength(p1,p2,p4);

		bool bFlag = dLen3<dLen4;
		double dLenMax = bFlag?dLen4:dLen3;
		double dLenMin = bFlag?dLen3:dLen4;
		double dNumMax = dLenMax/dDis;
		double dNumMin = dLenMin/dDis;
		int iLineNumMax = (int)floor(dNumMax);
		int iLineNumMin = (int)floor(dNumMin);
        bool bMax = fabs(iLineNumMax-dNumMax) < g_dEPS;
        bool bMin = fabs(iLineNumMin-dNumMin) < g_dEPS;
		if (bMax)//如果刚好平均分，减少一条直线
		{
			iLineNumMax--;
		}

		if (bMin)//如果刚好平均分，减少一条直线
		{
			iLineNumMin--;
		}

		if (iLineNumMax < 1)
		{
			return arrValue;
		}

		//以下获取长端分割点
		//ptEndL、ptBeginL、ptEndS、ptBeginS：长短端的起始点与终止点
		TXNPoint ptEndL = bFlag?p4:p3;
		TXNPoint ptBeginL = bFlag?p1:p2;

		TXNPoint ptEndS = bFlag?p3:p4;
		TXNPoint ptBeginS = bFlag?p2:p1;

		//长端
		double dAL = GetLineParaA(ptBeginL,ptEndL);
		double dBL = GetLineParaB(ptBeginL,ptEndL);
		double dCL = GetLineParaC(ptBeginL,ptEndL);

		//短端
		double dAS = GetLineParaA(ptBeginS,ptEndS);
		double dBS = GetLineParaB(ptBeginS,ptEndS);
		double dCS = GetLineParaC(ptBeginS,ptEndS);

		//对端 opposite
		double dAO = GetLineParaA(ptEndL,ptEndS);
		double dBO = GetLineParaB(ptEndL,ptEndS);
		double dCO = GetLineParaC(ptEndL,ptEndS);
		
		arrValue.push_back(p1);
		arrValue.push_back(p2);

		for (int i = 0; i < iLineNumMax; i++)
		{
			//生成较长的垂线的切割平行线，iLineNumMax条平行线 一般式为dAP*x+dBP*y+dCP=0;
			double dAP = GetLineParaA(p1,p2);
			double dBP = GetLineParaB(p1,p2);
			double dCP = GetLineParaC(p1,p2,ptEndL,dDis*(i+1));

			//p1p2平行线与长端交点
			TXNPoint ptIntersectL = GetIntersectPoint(dAP, dBP, dCP, dAL, dBL, dCL);
			TXNPoint ptIntersectS;

			//p1p2平行线与短端交点
			if (i < iLineNumMin)
			{
				ptIntersectS = GetIntersectPoint(dAP, dBP, dCP, dAS, dBS, dCS);
			}
			else
			{
				ptIntersectS = GetIntersectPoint(dAP, dBP, dCP, dAO, dBO, dCO);
			}
			if (i == iLineNumMin)
			{
				TXNPoint ptTmp = *arrValue.rbegin();
				double dTmpS = dAS*ptTmp.first+dBS*ptTmp.second+dCS;
				double dTmpL = dAL*ptTmp.first+dBL*ptTmp.second+dCL;
				if (fabs(dTmpS) < fabs(dTmpL))
				{
					arrValue.push_back(ptEndS);
				}			
			}


			if (bFlag)//如果距离p4较远 先压入p2p3中的点
			{
				arrValue.push_back(ptIntersectS);
				arrValue.push_back(ptIntersectL);
			}
			else
			{
				arrValue.push_back(ptIntersectL);
				arrValue.push_back(ptIntersectS);
			}

			bFlag = !bFlag;
		}

		//如果相交ptEndL在最后，否则要判断ptEndL ptEndS谁在最后
		if (iLineNumMin != iLineNumMax)
		{
			arrValue.push_back(ptEndL);
		}
		else
		{
			TXNPoint ptTmp = *arrValue.rbegin();

			//判断最后一个点是否在长端直线上
            double dTmpL = dAL*ptTmp.first+dBL*ptTmp.second+dCL;
            double dTmpS = dAS*ptTmp.first+dBS*ptTmp.second+dCS;

            //精度要比较高
            if (fabs(dTmpL) < fabs(dTmpS))
            {
                arrValue.push_back(ptEndL);
                arrValue.push_back(ptEndS);
            }
            else
            {
                arrValue.push_back(ptEndS);
                arrValue.push_back(ptEndL);
            }
		}

		return arrValue;
	}


 }
