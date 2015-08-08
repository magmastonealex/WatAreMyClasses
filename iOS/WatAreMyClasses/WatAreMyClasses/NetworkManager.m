//
//  NetworkManager.m
//  WatAreMyClasses
//
//  Created by Alex Roth on 2015-08-07.
//  Copyright © 2015 Alex Roth. All rights reserved.
//

#import "NetworkManager.h"
#import "WatBuilding.h"
#import "WatClass.h"
#import "WatNode.h"
//Basic abstraction/mapping object for Overcoat.
@implementation NetworkManager

+ (NSDictionary *)modelClassesByResourcePath {
    return @{
             @"getpath": [WatNode class],
             @"getschedule": [WatClass class],
             @"getnextclass": [WatClass class],
             @"getclosestnode": [WatNode class],
             @"buildinglist": [WatBuilding class]
             };
}

@end
