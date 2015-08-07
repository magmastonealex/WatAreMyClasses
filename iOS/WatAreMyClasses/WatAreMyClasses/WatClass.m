//
//  WatClass.m
//  WatAreMyClasses
//
//  Created by Alex Roth on 2015-08-07.
//  Copyright © 2015 Alex Roth. All rights reserved.
//  This is a basic

#import "WatClass.h"


//This is a basic container that represents a single class.

@implementation WatClass
@synthesize cid,class_name,section,timestamp,timeend,instructor,type,where;

+ (NSDictionary *)JSONKeyPathsByPropertyKey {
    return @{
             @"cid": @"id",
             @"class_name": @"class_name",
             @"timestamp": @"timestamp",
             @"timeend": @"timeend",
             @"instructor": @"instructor",
             @"type": @"type",
             @"where": @"where"
             };
}

@end
