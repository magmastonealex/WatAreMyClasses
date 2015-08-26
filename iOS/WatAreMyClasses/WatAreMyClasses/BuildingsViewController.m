//
//  BuildingsViewController.m
//  WatAreMyClasses
//
//  Created by Alex Roth on 2015-08-11.
//  Copyright © 2015 Alex Roth. All rights reserved.
//

#import "BuildingsViewController.h"
#import "DataCacher.h"
#import "WatBuilding.h"
@interface BuildingsViewController ()
@property (nonatomic) NSArray * classesArray;

@end

@implementation BuildingsViewController
@synthesize classesArray,doneGoto;

- (void)viewDidLoad {
    [super viewDidLoad];
    DataCacher * sCache=[DataCacher sharedCache];
    classesArray=sCache.buildings;
    doneGoto=@"none";
    // Do any additional setup after loading the view.
}
-(void)viewDidAppear:(BOOL)animated{
    [super viewDidAppear:animated];
    if (classesArray==nil){
        [self performSegueWithIdentifier:@"LeaveBuildings" sender:self];
    }
}
- (void)didReceiveMemoryWarning {
    [super didReceiveMemoryWarning];
    // Dispose of any resources that can be recreated.
}

-(void)tableView:(UITableView *)tableView didSelectRowAtIndexPath:(NSIndexPath *)indexPath{
    NSString *bid = ((WatBuilding*)[classesArray objectAtIndex:indexPath.row]).bid;
    doneGoto=[NSString stringWithFormat:@"b-%@",bid];
    [self performSegueWithIdentifier:@"LeaveBuildings" sender:self];
}
- (NSInteger)tableView:(UITableView *)tableView numberOfRowsInSection:(NSInteger)section
{
    return [classesArray count];
}

- (UITableViewCell *)tableView:(UITableView *)tableView cellForRowAtIndexPath:(NSIndexPath *)indexPath
{
    static NSString *simpleTableIdentifier = @"BuildingCell";
    
    UITableViewCell *cell = [tableView dequeueReusableCellWithIdentifier:simpleTableIdentifier];
    
    if (cell == nil) {
        cell = [[UITableViewCell alloc] initWithStyle:UITableViewCellStyleDefault reuseIdentifier:simpleTableIdentifier];
    }
    WatBuilding * cls = [classesArray objectAtIndex:indexPath.row];
    
    UILabel * firstLine = (UILabel *)[cell viewWithTag:5]; //First line
    UILabel * secondLine = (UILabel *)[cell viewWithTag:10]; //second line
    [firstLine setText:cls.name];
    [secondLine setText:cls.bid];
    return cell;
}

/*
#pragma mark - Navigation

// In a storyboard-based application, you will often want to do a little preparation before navigation
- (void)prepareForSegue:(UIStoryboardSegue *)segue sender:(id)sender {
    // Get the new view controller using [segue destinationViewController].
    // Pass the selected object to the new view controller.
}
*/

@end
